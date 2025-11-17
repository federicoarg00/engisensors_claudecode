"""
MQTT Handler Service
Connects to MQTT broker and processes sensor messages
"""
import json
import logging
import threading
from datetime import datetime
from typing import Optional, Callable, Dict, Any

import paho.mqtt.client as mqtt
from app.config import settings

logger = logging.getLogger(__name__)


class MQTTService:
    """
    MQTT Service for handling sensor communications.

    Connects to the MQTT broker at www.trustcapsupes.com and subscribes
    to sensor topics to receive gas detection data in real-time.
    """

    def __init__(self):
        self.client: Optional[mqtt.Client] = None
        self._connected = False
        self._lock = threading.Lock()
        self.message_handlers: Dict[str, Callable] = {}

    def _on_connect(self, client, userdata, flags, rc):
        """
        Callback when client connects to MQTT broker.

        Args:
            rc: Result code (0 = success)
        """
        if rc == 0:
            self._connected = True
            logger.info(f"✅ Connected to MQTT broker: {settings.mqtt_broker_host}")

            # Subscribe to all sensor topics
            topic = settings.mqtt_base_topic
            client.subscribe(topic, qos=settings.mqtt_qos)
            logger.info(f"📡 Subscribed to topic: {topic}")
        else:
            self._connected = False
            error_messages = {
                1: "Incorrect protocol version",
                2: "Invalid client identifier",
                3: "Server unavailable",
                4: "Bad username or password",
                5: "Not authorized"
            }
            error_msg = error_messages.get(rc, f"Unknown error code: {rc}")
            logger.error(f"❌ Failed to connect to MQTT broker: {error_msg}")

    def _on_disconnect(self, client, userdata, rc):
        """Callback when client disconnects from MQTT broker."""
        self._connected = False
        if rc != 0:
            logger.warning(f"⚠️ Unexpected disconnection from MQTT broker. Code: {rc}")
        else:
            logger.info("🔌 Disconnected from MQTT broker")

    def _on_message(self, client, userdata, msg):
        """
        Callback when a message is received from MQTT broker.

        Expected topic format: engisensors/{client_id}/{building_id}/{apartment_id}/{sensor_id}/status
        Expected payload: JSON with sensor data
        """
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')

            logger.debug(f"📨 Received MQTT message on topic: {topic}")
            logger.debug(f"Payload: {payload}")

            # Parse JSON payload
            try:
                data = json.loads(payload)
            except json.JSONDecodeError as e:
                logger.error(f"❌ Invalid JSON payload: {e}")
                logger.error(f"Payload was: {payload}")
                return

            # Validate message structure
            if not self._validate_message(data):
                logger.error(f"❌ Invalid message structure: {data}")
                return

            # Add metadata
            data['mqtt_topic'] = topic
            data['received_at'] = datetime.utcnow().isoformat()

            # Process the sensor message
            self._process_sensor_message(topic, data)

        except Exception as e:
            logger.exception(f"❌ Error processing MQTT message: {e}")

    def _validate_message(self, data: Dict[str, Any]) -> bool:
        """
        Validate sensor message structure.

        Required fields:
        - sensor_id: str
        - timestamp: str (ISO format)
        - status: str (normal, alert, warning, offline)
        - gas_level: int/float (PPM)

        Optional fields:
        - threshold: int/float
        - battery: int (percentage)
        - signal_strength: int (dBm)
        """
        required_fields = ['sensor_id', 'timestamp', 'status', 'gas_level']

        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field: {field}")
                return False

        # Validate status values
        valid_statuses = ['normal', 'alert', 'warning', 'offline', 'online']
        if data['status'] not in valid_statuses:
            logger.error(f"Invalid status: {data['status']}. Must be one of {valid_statuses}")
            return False

        # Validate gas_level range (0-10000 PPM typical for combustible gas)
        gas_level = data.get('gas_level')
        if not isinstance(gas_level, (int, float)):
            logger.error(f"Invalid gas_level type: {type(gas_level)}")
            return False

        if not 0 <= gas_level <= 10000:
            logger.warning(f"⚠️ Gas level out of typical range: {gas_level} PPM")
            # Don't reject, just warn

        return True

    def _process_sensor_message(self, topic: str, data: Dict[str, Any]):
        """
        Process validated sensor message.

        This is where we handle:
        1. Storing sensor data to database
        2. Checking thresholds and triggering alerts
        3. Broadcasting to WebSocket clients
        """
        sensor_id = data['sensor_id']
        status = data['status']
        gas_level = data['gas_level']
        threshold = data.get('threshold', settings.default_gas_threshold_ppm)

        logger.info(f"🔍 Processing sensor {sensor_id}: {status}, {gas_level} PPM")

        # Check if gas level exceeds threshold
        if status == 'alert' or gas_level >= threshold:
            logger.critical(f"🚨 GAS ALERT! Sensor {sensor_id} detected {gas_level} PPM (threshold: {threshold})")
            # TODO: Trigger notification workflow
            # TODO: Store alert event in database
            # TODO: Broadcast to WebSocket clients

        # TODO: Store sensor event in TimescaleDB
        # TODO: Update sensor last_seen timestamp
        # TODO: Update sensor status

        # Call registered message handlers
        for handler_name, handler_func in self.message_handlers.items():
            try:
                handler_func(topic, data)
            except Exception as e:
                logger.error(f"Error in message handler '{handler_name}': {e}")

    def register_message_handler(self, name: str, handler: Callable):
        """
        Register a custom message handler.

        Args:
            name: Unique name for the handler
            handler: Function(topic: str, data: dict) to process messages
        """
        self.message_handlers[name] = handler
        logger.info(f"Registered message handler: {name}")

    def start(self):
        """Start the MQTT client and connect to broker."""
        with self._lock:
            if self.client is not None:
                logger.warning("MQTT client already running")
                return

            # Create MQTT client
            self.client = mqtt.Client(
                client_id=settings.mqtt_client_id,
                clean_session=True,
                protocol=mqtt.MQTTv311
            )

            # Set authentication if provided
            if settings.mqtt_broker_username and settings.mqtt_broker_password:
                self.client.username_pw_set(
                    settings.mqtt_broker_username,
                    settings.mqtt_broker_password
                )
                logger.info("🔐 MQTT authentication configured")

            # Set callbacks
            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            self.client.on_message = self._on_message

            # Connect to broker
            try:
                logger.info(f"🔌 Connecting to MQTT broker: {settings.mqtt_broker_host}:{settings.mqtt_broker_port}")
                self.client.connect(
                    settings.mqtt_broker_host,
                    settings.mqtt_broker_port,
                    settings.mqtt_keepalive
                )

                # Start network loop in background thread
                self.client.loop_start()
                logger.info("✅ MQTT client loop started")

            except Exception as e:
                logger.error(f"❌ Failed to connect to MQTT broker: {e}")
                self.client = None
                raise

    def stop(self):
        """Stop the MQTT client."""
        with self._lock:
            if self.client is None:
                return

            try:
                self.client.loop_stop()
                self.client.disconnect()
                self.client = None
                self._connected = False
                logger.info("🛑 MQTT client stopped")
            except Exception as e:
                logger.error(f"Error stopping MQTT client: {e}")

    def is_connected(self) -> bool:
        """Check if client is connected to broker."""
        return self._connected

    def publish(self, topic: str, payload: dict, qos: int = None):
        """
        Publish a message to MQTT broker.

        Args:
            topic: MQTT topic
            payload: Dictionary to send as JSON
            qos: Quality of Service level (0, 1, or 2)
        """
        if not self.client or not self._connected:
            logger.error("Cannot publish: MQTT client not connected")
            return False

        try:
            qos = qos if qos is not None else settings.mqtt_qos
            message = json.dumps(payload)
            result = self.client.publish(topic, message, qos=qos)

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.debug(f"📤 Published to {topic}: {message}")
                return True
            else:
                logger.error(f"Failed to publish to {topic}: {result.rc}")
                return False
        except Exception as e:
            logger.error(f"Error publishing message: {e}")
            return False


# Global MQTT service instance
mqtt_service = MQTTService()
