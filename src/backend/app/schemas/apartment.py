"""
Apartment Pydantic Schemas

Request/response models for apartment endpoints.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class ApartmentBase(BaseModel):
    """Base apartment schema with common fields."""
    number: str = Field(..., min_length=1, max_length=50, description="Apartment number (e.g., '101', '2A')")
    floor: Optional[int] = Field(None, ge=0, description="Floor number")
    description: Optional[str] = Field(None, description="Additional description")


class ApartmentCreate(ApartmentBase):
    """Schema for creating a new apartment."""
    building_id: UUID = Field(..., description="UUID of the building")


class ApartmentUpdate(BaseModel):
    """Schema for updating apartment information."""
    number: Optional[str] = Field(None, min_length=1, max_length=50)
    floor: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None


class ApartmentResponse(ApartmentBase):
    """Schema for apartment response."""
    id: UUID
    building_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ApartmentWithStats(ApartmentResponse):
    """Schema for apartment with sensor statistics."""
    building_name: Optional[str] = None
    total_locations: int = 0
    total_sensors: int = 0
    online_sensors: int = 0
    failure_sensors: int = 0
    alert_sensors: int = 0
    disconnected_sensors: int = 0
