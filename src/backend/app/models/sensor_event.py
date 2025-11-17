"""
Sensor Event Model
Time-series data from gas sensors (TimescaleDB hypertable)
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from sqlalchemy.orm import relationship
import uuid
import enum

from app.database import Base


class EventType(str, enum.Enum):
    """Types of sensor events."""
    NORMAL = "normal"      # Normal gas levels
    ALERT = "alert"        # Gas threshold exceeded!
    WARNING = "warning"    # Approaching threshold
    OFFLINE = "offline"    # Sensor went offline
    ONLINE = "online"      # Sensor came online


class SensorEvent(Base):
    """
    Sensor Event model - time-series data from gas sensors.

    This table will be converted to a TimescaleDB hypertable for efficient
    time-series queries and automatic data compression/retention.

    Stores all sensor readings with timestamp for historical analysis.
    """
    __tablename__ = "sensor_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_id = Column(UUID(as_uuid=True), ForeignKey("sensors.id"), nullable=False, index=True)

    event_type = Column(Enum(EventType), nullable=False, index=True)

    # Gas measurement data
    gas_level = Column(Integer, nullable=True)  # PPM (parts per million)
    threshold = Column(Integer, nullable=True)   # Threshold at time of reading

    # Sensor health at time of event
    battery_level = Column(Integer, nullable=True)   # 0-100%
    signal_strength = Column(Integer, nullable=True)  # dBm

    # Raw MQTT message data (for debugging and future extensibility)
    raw_data = Column(JSONB, nullable=True)

    # Timestamp - PRIMARY dimension for TimescaleDB
    timestamp = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        index=True,
        primary_key=True  # Part of composite primary key with id
    )

    # Relationships
    sensor = relationship("Sensor", back_populates="events")
    notifications = relationship("Notification", back_populates="event", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<SensorEvent {self.event_type} at {self.timestamp}>"
