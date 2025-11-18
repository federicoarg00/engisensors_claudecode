"""
Location Pydantic Schemas

Request/response models for location endpoints.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from app.models.location import LocationType


class LocationBase(BaseModel):
    """Base location schema with common fields."""
    location_type: LocationType = Field(..., description="Type of location (cocina, lavadero, etc.)")
    description: Optional[str] = Field(None, description="Additional description")


class LocationCreate(LocationBase):
    """Schema for creating a new location."""
    apartment_id: UUID = Field(..., description="UUID of the apartment")


class LocationUpdate(BaseModel):
    """Schema for updating location information."""
    location_type: Optional[LocationType] = None
    description: Optional[str] = None


class LocationResponse(LocationBase):
    """Schema for location response."""
    id: UUID
    apartment_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LocationWithSensor(LocationResponse):
    """Schema for location with sensor information."""
    apartment_number: Optional[str] = None
    building_name: Optional[str] = None
    client_name: Optional[str] = None
    has_sensor: bool = False
    sensor_id: Optional[UUID] = None
    sensor_device_id: Optional[str] = None
    sensor_status: Optional[str] = None
