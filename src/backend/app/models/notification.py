"""
Notification Model
Track alert notifications sent to contacts
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum

from app.database import Base


class NotificationChannel(str, enum.Enum):
    """Notification delivery channels."""
    EMAIL = "email"
    SMS = "sms"


class NotificationStatus(str, enum.Enum):
    """Notification delivery status."""
    PENDING = "pending"      # Queued for delivery
    SENT = "sent"            # Sent to provider
    DELIVERED = "delivered"  # Confirmed delivered
    FAILED = "failed"        # Delivery failed


class Notification(Base):
    """
    Notification model - tracks alert notifications sent to contacts.

    Records all notification attempts for audit trail and debugging.
    """
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("sensor_events.id"), nullable=False, index=True)
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"), nullable=False, index=True)

    channel = Column(Enum(NotificationChannel), nullable=False, index=True)
    status = Column(Enum(NotificationStatus), nullable=False, default=NotificationStatus.PENDING, index=True)

    # External provider tracking
    message_id = Column(String(255), nullable=True)  # Provider's message ID
    error_message = Column(Text, nullable=True)      # Error details if failed

    # Timestamps
    sent_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    event = relationship("SensorEvent", back_populates="notifications")
    contact = relationship("Contact", back_populates="notifications")

    def __repr__(self):
        return f"<Notification {self.channel} to {self.contact_id} ({self.status})>"
