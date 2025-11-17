"""
Contact Model
Email and phone contacts for notifications
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum

from app.database import Base


class ContactType(str, enum.Enum):
    """Types of contact methods."""
    EMAIL = "email"
    PHONE = "phone"  # For SMS


class Contact(Base):
    """
    Contact model - email and phone numbers for alert notifications.

    Each client can have multiple contacts who will receive alerts
    when gas is detected.
    """
    __tablename__ = "contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, index=True)

    type = Column(Enum(ContactType), nullable=False, index=True)
    value = Column(String(255), nullable=False)  # Email address or phone number

    label = Column(String(100), nullable=True)  # e.g., "Gerente", "Seguridad", "Mantenimiento"
    is_primary = Column(Boolean, default=False, nullable=False)  # Primary contact
    is_active = Column(Boolean, default=True, nullable=False)    # Can be disabled without deleting
    verified = Column(Boolean, default=False, nullable=False)    # Email/phone verified

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    client = relationship("Client", back_populates="contacts")
    notifications = relationship("Notification", back_populates="contact", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Contact {self.type}: {self.value}>"
