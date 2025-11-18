"""
Sensor Utility Functions

Helper functions for sensor status, disconnection detection, and battery monitoring.
"""
from datetime import datetime, timedelta
from typing import Optional, Tuple
from app.config import settings
from app.models.sensor import Sensor, SensorStatus


def is_sensor_disconnected(last_seen: Optional[datetime]) -> bool:
    """
    Determine if a sensor is disconnected based on last_seen timestamp.

    A sensor is considered disconnected if it hasn't reported status within
    the configured disconnection timeout (default: 6 hours).

    Args:
        last_seen: Last timestamp when sensor reported status

    Returns:
        True if sensor is disconnected, False otherwise
    """
    if not last_seen:
        # Never seen = disconnected
        return True

    timeout_hours = settings.sensor_disconnection_timeout_hours
    disconnection_threshold = datetime.utcnow() - timedelta(hours=timeout_hours)

    return last_seen < disconnection_threshold


def get_computed_sensor_status(sensor: Sensor) -> Tuple[str, str]:
    """
    Compute the actual sensor status considering multiple factors.

    Returns a tuple of (status, category) where:
    - status: The actual operational status (online/disconnected/alert/failure)
    - category: Category for statistics (online/disconnected/alert/failure)

    Logic:
    1. Check if disconnected (last_seen > 6 hours) -> disconnected
    2. Check if detecting gas (status=ALERT) -> alert
    3. Check if in maintenance (status=MAINTENANCE) -> failure
    4. Check battery level:
       - Critical (< 10%) -> failure
       - Low (< 20%) -> failure (warning level)
    5. Otherwise -> online

    Args:
        sensor: Sensor model instance

    Returns:
        Tuple[str, str]: (status description, category)
    """
    # Check disconnection first
    if is_sensor_disconnected(sensor.last_seen):
        return ("Desconectado", "disconnected")

    # Check alert status (gas detection)
    if sensor.status == SensorStatus.ALERT:
        return ("Alerta - Gas Detectado", "alert")

    # Check maintenance/failure status
    if sensor.status == SensorStatus.MAINTENANCE:
        return ("En Falla - Mantenimiento Requerido", "failure")

    # Check battery level
    if sensor.battery_level is not None:
        if sensor.battery_level <= settings.battery_critical_threshold_percent:
            return (f"En Falla - Batería Crítica ({sensor.battery_level}%)", "failure")
        elif sensor.battery_level <= settings.battery_low_threshold_percent:
            return (f"En Falla - Batería Baja ({sensor.battery_level}%)", "failure")

    # Check if inactive
    if sensor.status == SensorStatus.INACTIVE:
        return ("Inactivo", "disconnected")

    # Otherwise, sensor is online and operational
    return ("En Línea", "online")


def get_battery_status(battery_level: Optional[int]) -> dict:
    """
    Get battery status information including health category.

    Args:
        battery_level: Battery percentage (0-100)

    Returns:
        dict with keys: level, status, color, icon
    """
    if battery_level is None:
        return {
            "level": None,
            "status": "Desconocido",
            "color": "gray",
            "icon": "❓"
        }

    if battery_level <= settings.battery_critical_threshold_percent:
        return {
            "level": battery_level,
            "status": "Crítico",
            "color": "red",
            "icon": "🔴"
        }
    elif battery_level <= settings.battery_low_threshold_percent:
        return {
            "level": battery_level,
            "status": "Bajo",
            "color": "orange",
            "icon": "🟠"
        }
    elif battery_level <= 50:
        return {
            "level": battery_level,
            "status": "Medio",
            "color": "yellow",
            "icon": "🟡"
        }
    else:
        return {
            "level": battery_level,
            "status": "Bueno",
            "color": "green",
            "icon": "🟢"
        }


def format_last_seen(last_seen: Optional[datetime]) -> str:
    """
    Format last_seen timestamp to human-readable string.

    Args:
        last_seen: Last seen timestamp

    Returns:
        Human-readable string like "Hace 5 minutos", "Hace 2 horas", etc.
    """
    if not last_seen:
        return "Nunca"

    delta = datetime.utcnow() - last_seen
    seconds = int(delta.total_seconds())

    if seconds < 60:
        return f"Hace {seconds} segundo{'s' if seconds != 1 else ''}"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"Hace {minutes} minuto{'s' if minutes != 1 else ''}"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"Hace {hours} hora{'s' if hours != 1 else ''}"
    else:
        days = seconds // 86400
        return f"Hace {days} día{'s' if days != 1 else ''}"


def should_send_heartbeat_warning(last_seen: Optional[datetime]) -> bool:
    """
    Determine if we should send a warning about missing heartbeat.

    Sends warning if sensor hasn't reported within expected interval
    but not yet considered fully disconnected.

    Args:
        last_seen: Last timestamp when sensor reported

    Returns:
        True if warning should be sent
    """
    if not last_seen:
        return False

    # Expected heartbeat interval + some grace period (e.g., 30% extra)
    expected_interval = settings.sensor_heartbeat_interval_minutes
    grace_period = int(expected_interval * 0.3)
    warning_threshold = datetime.utcnow() - timedelta(minutes=expected_interval + grace_period)

    # Warn if exceeded expected interval but not yet disconnected
    return (
        last_seen < warning_threshold
        and not is_sensor_disconnected(last_seen)
    )
