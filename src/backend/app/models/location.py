"""
Location Model
Specific rooms/areas within apartments where sensors are placed
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum

from app.database import Base


class LocationType(str, enum.Enum):
    """Types of locations where sensors can be placed."""
    COCINA = "cocina"          # Kitchen
    LAVADERO = "lavadero"      # Laundry room
    SALA = "sala"              # Living room
    RECAMARA = "recamara"      # Bedroom
    BANO = "baño"              # Bathroom
    GARAJE = "garaje"          # Garage
    BODEGA = "bodega"          # Storage
    PASILLO = "pasillo"        # Hallway
    OTRO = "otro"              # Other


class Location(Base):
    """
    Location model - specific rooms/areas within apartments.

    Hierarchy: Client → Building → Apartment → Location → Sensor

    Common locations: cocina (kitchen), lavadero (laundry),
    sala (living room), recámara (bedroom), etc.
    """
    __tablename__ = "locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apartment_id = Column(UUID(as_uuid=True), ForeignKey("apartments.id", ondelete="CASCADE"), nullable=False, index=True)

    location_type = Column(Enum(LocationType), nullable=False)
    description = Column(Text, nullable=True)  # Additional details

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete

    # Relationships
    apartment = relationship("Apartment", back_populates="locations")
    sensors = relationship("Sensor", back_populates="location", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Location {self.location_type}>"
