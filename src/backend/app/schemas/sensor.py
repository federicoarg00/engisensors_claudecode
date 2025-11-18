"""
Sensor Pydantic Schemas

Request/response models for sensor endpoints.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from app.models.sensor import SensorStatus


class SensorBase(BaseModel):
    """Base sensor schema with common fields."""
    device_id: str = Field(..., min_length=1, max_length=100, description="Unique device identifier")
    model: Optional[str] = Field(None, max_length=100, description="Sensor model name")
    firmware_version: Optional[str] = Field(None, max_length=50, description="Firmware version")
    gas_threshold_ppm: int = Field(800, ge=0, le=10000, description="Gas alert threshold in PPM")


class SensorCreate(SensorBase):
    """Schema for creating a new sensor."""
    location_id: UUID = Field(..., description="UUID of the location where sensor is installed")


class SensorUpdate(BaseModel):
    """Schema for updating sensor information."""
    model: Optional[str] = Field(None, max_length=100)
    firmware_version: Optional[str] = Field(None, max_length=50)
    gas_threshold_ppm: Optional[int] = Field(None, ge=0, le=10000)
    status: Optional[SensorStatus] = None
    location_id: Optional[UUID] = None


class SensorResponse(SensorBase):
    """Schema for sensor response."""
    id: UUID
    status: SensorStatus
    battery_level: Optional[int] = Field(None, ge=0, le=100)
    signal_strength: Optional[int] = Field(None, description="Signal strength in dBm")
    last_seen: Optional[datetime] = None
    location_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SensorWithLocation(SensorResponse):
    """Schema for sensor with location details."""
    location: Optional[dict] = None
    apartment: Optional[dict] = None
    building: Optional[dict] = None
    client: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)


class SensorStatusUpdate(BaseModel):
    """Schema for updating sensor status only."""
    status: SensorStatus
    battery_level: Optional[int] = Field(None, ge=0, le=100)
    signal_strength: Optional[int] = None


class SensorCodeValidation(BaseModel):
    """Schema for validating a sensor code."""
    device_id: str = Field(
        ...,
        min_length=10,
        max_length=10,
        pattern="^[A-Za-z0-9]{10}$",
        description="Unique 10-character alphanumeric sensor code"
    )


class SensorCodeValidationResponse(BaseModel):
    """Response for sensor code validation."""
    valid: bool
    available: bool
    device_id: str
    message: str
    # Pre-filled info if sensor is in inventory (future feature)
    suggested_model: Optional[str] = None
    suggested_threshold: int = 800


class SensorProvision(BaseModel):
    """Schema for provisioning/registering a new sensor with full hierarchy."""
    device_id: str = Field(
        ...,
        min_length=10,
        max_length=10,
        pattern="^[A-Za-z0-9]{10}$",
        description="Unique 10-character alphanumeric sensor code"
    )
    location_id: UUID = Field(..., description="UUID of the location where sensor is installed")
    gas_threshold_ppm: int = Field(800, ge=100, le=10000, description="Gas alert threshold in PPM")
    model: Optional[str] = Field("MQ-2 Gas Detector", max_length=100, description="Sensor model name")
    firmware_version: Optional[str] = Field("v2.1.0", max_length=50, description="Firmware version")


class SensorProvisionResponse(SensorResponse):
    """Response for sensor provisioning including hierarchy info."""
    location_type: Optional[str] = None
    apartment_number: Optional[str] = None
    building_name: Optional[str] = None
    client_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
