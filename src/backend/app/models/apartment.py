"""
Apartment Model
Individual units within buildings
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class Apartment(Base):
    """
    Apartment/Unit model - individual living spaces within buildings.

    Hierarchy: Client → Building → Apartment → Location → Sensor
    """
    __tablename__ = "apartments"
    __table_args__ = (
        UniqueConstraint('building_id', 'number', name='unique_building_apartment'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    building_id = Column(UUID(as_uuid=True), ForeignKey("buildings.id", ondelete="CASCADE"), nullable=False, index=True)

    number = Column(String(50), nullable=False)  # Apartment number (e.g., "101", "2A")
    floor = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete

    # Relationships
    building = relationship("Building", back_populates="apartments")
    locations = relationship("Location", back_populates="apartment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Apartment {self.number}>"
