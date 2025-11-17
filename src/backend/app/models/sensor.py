"""
Sensor Model
IoT gas detection devices
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum

from app.database import Base


class SensorStatus(str, enum.Enum):
    """Sensor operational status."""
    ACTIVE = "active"              # Normal operation
    INACTIVE = "inactive"          # Manually disabled
    ALERT = "alert"                # Gas detected!
    MAINTENANCE = "maintenance"    # Under maintenance
    DISCONNECTED = "disconnected"  # Not communicating


class Sensor(Base):
    """
    Sensor model - IoT gas detection devices.

    Hierarchy: Client → Building → Apartment → Location → Sensor

    Each sensor monitors gas levels and sends alerts when thresholds are exceeded.
    """
    __tablename__ = "sensors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id", ondelete="CASCADE"), nullable=False, index=True)

    device_id = Column(String(100), unique=True, nullable=False, index=True)  # Unique hardware ID
    model = Column(String(100), nullable=True)
    firmware_version = Column(String(50), nullable=True)

    status = Column(
        Enum(SensorStatus),
        nullable=False,
        default=SensorStatus.ACTIVE,
        index=True
    )

    # Installation and maintenance tracking
    installed_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_maintenance = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)  # Last communication from sensor

    # Sensor health metrics
    battery_level = Column(Integer, nullable=True)  # 0-100%
    signal_strength = Column(Integer, nullable=True)  # dBm

    # Configuration
    gas_threshold_ppm = Column(Integer, nullable=False, default=800)  # Alert threshold

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete

    # Relationships
    location = relationship("Location", back_populates="sensors")
    events = relationship("SensorEvent", back_populates="sensor", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Sensor {self.device_id} ({self.status})>"
