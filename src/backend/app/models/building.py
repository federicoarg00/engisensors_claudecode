"""
Building Model
Physical properties where sensors are deployed
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.database import Base
from app.models.associations import building_admins


class Building(Base):
    """
    Building model - physical properties containing apartments/units.

    Hierarchy: Client → Building → Apartment → Location → Sensor
    """
    __tablename__ = "buildings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, index=True)
    admin_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)

    # Geographic coordinates for mapping (future feature)
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(11, 8), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete

    # Relationships
    client = relationship("Client", back_populates="buildings")
    admin = relationship("User", foreign_keys=[admin_id])  # Deprecated: use admins instead
    apartments = relationship("Apartment", back_populates="building", cascade="all, delete-orphan")

    # Many-to-many relationship with building administrators
    admins = relationship(
        "User",
        secondary=building_admins,
        backref="managed_buildings",
        lazy="select"
    )

    def __repr__(self):
        return f"<Building {self.name}>"
