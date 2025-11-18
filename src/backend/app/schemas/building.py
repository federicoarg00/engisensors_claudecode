"""
Building Pydantic Schemas

Request/response models for building endpoints.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class BuildingBase(BaseModel):
    """Base building schema with common fields."""
    name: str = Field(..., min_length=1, max_length=255, description="Building name")
    address: str = Field(..., min_length=1, description="Building address")
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    latitude: Optional[Decimal] = Field(None, ge=-90, le=90)
    longitude: Optional[Decimal] = Field(None, ge=-180, le=180)


class BuildingCreate(BuildingBase):
    """Schema for creating a new building."""
    client_id: UUID = Field(..., description="UUID of the client that owns this building")
    admin_id: Optional[UUID] = Field(None, description="UUID of the building administrator")


class BuildingUpdate(BaseModel):
    """Schema for updating building information."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    address: Optional[str] = Field(None, min_length=1)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    latitude: Optional[Decimal] = Field(None, ge=-90, le=90)
    longitude: Optional[Decimal] = Field(None, ge=-180, le=180)
    admin_id: Optional[UUID] = Field(None, description="UUID of the building administrator")


class BuildingResponse(BuildingBase):
    """Schema for building response."""
    id: UUID
    client_id: UUID
    admin_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BuildingWithAdmin(BuildingResponse):
    """Schema for building with admin information."""
    admin_name: Optional[str] = None
    admin_email: Optional[str] = None


class BuildingWithStats(BuildingResponse):
    """Schema for building with sensor statistics - 5 categories."""
    client_name: Optional[str] = None
    admin_name: Optional[str] = None
    admin_email: Optional[str] = None
    total_apartments: int = 0
    total_sensors: int = 0  # Sensores instalados (total)
    online_sensors: int = 0  # Sensores en línea (operational)
    failure_sensors: int = 0  # Sensores en falla técnica
    alert_sensors: int = 0  # Sensores detectando gas
    disconnected_sensors: int = 0  # Sensores desconectados


class ApartmentSensorInfo(BaseModel):
    """Schema for apartment with its sensors."""
    apartment_id: UUID
    apartment_number: str
    floor: Optional[int] = None
    sensors: List["SensorWithComputedStatus"] = []


class SensorWithComputedStatus(BaseModel):
    """Schema for sensor with computed status based on disconnection logic."""
    id: UUID
    device_id: str
    model: Optional[str] = None
    firmware_version: Optional[str] = None
    gas_threshold_ppm: int
    battery_level: Optional[int] = None
    signal_strength: Optional[int] = None
    last_seen: Optional[datetime] = None
    location_id: UUID
    location_type: str  # cocina, lavadero, etc.

    # Computed status fields
    status_category: str  # online, alert, failure, disconnected
    status_description: str  # Human-readable status

    # Original database status for reference
    db_status: str

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BuildingWithSensors(BuildingResponse):
    """Schema for building with all its sensors organized by apartment."""
    client_name: Optional[str] = None
    apartments: List[ApartmentSensorInfo] = []

    # Statistics summary
    total_sensors: int = 0
    online_sensors: int = 0
    failure_sensors: int = 0
    alert_sensors: int = 0
    disconnected_sensors: int = 0


# Update forward references
ApartmentSensorInfo.model_rebuild()
