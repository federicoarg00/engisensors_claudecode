"""
User Model
Handles authentication for both admins and clients
"""
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum

from app.database import Base


class UserRole(str, enum.Enum):
    """User roles in the system."""
    ADMIN = "admin"                    # System administrator - full access
    BUILDING_ADMIN = "building_admin"  # Building administrator - manages buildings
    OWNER = "owner"                    # Apartment owner - owns apartments, can add residents
    RESIDENT = "resident"              # Apartment resident - lives in apartment, added by owner


class User(Base):
    """
    User model for authentication.

    Roles:
    - admin: Full system access, can manage all clients and sensors
    - building_admin: Manages one or multiple buildings, receives all notifications from their buildings
    - owner: Owns apartment(s), can add residents, receives notifications from their sensors
    - resident: Lives in apartment(s), added by owner, receives notifications from apartment sensors
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    client = relationship("Client", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
