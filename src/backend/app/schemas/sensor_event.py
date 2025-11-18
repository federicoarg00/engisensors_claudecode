"""
Sensor Event Pydantic Schemas

Request/response models for sensor event endpoints.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from app.models.sensor_event import EventType


class SensorEventBase(BaseModel):
    """Base sensor event schema."""
    event_type: EventType
    gas_level: Optional[int] = Field(None, ge=0, le=10000, description="Gas level in PPM")
    threshold: Optional[int] = Field(None, ge=0, le=10000, description="Threshold at time of event")
    battery_level: Optional[int] = Field(None, ge=0, le=100, description="Battery percentage")
    signal_strength: Optional[int] = Field(None, description="Signal strength in dBm")
    timestamp: datetime


class SensorEventResponse(SensorEventBase):
    """Schema for sensor event response."""
    id: UUID
    sensor_id: UUID
    raw_data: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)


class SensorEventWithLocation(SensorEventResponse):
    """Schema for sensor event with sensor location details."""
    sensor_device_id: Optional[str] = None
    location_type: Optional[str] = None
    apartment_number: Optional[str] = None
    building_name: Optional[str] = None
    client_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class SensorStatsResponse(BaseModel):
    """Schema for sensor statistics and metadata."""
    sensor_id: UUID
    device_id: str
    activation_date: datetime  # Created_at from sensor
    days_active: int  # Calculated from activation_date
    current_status: str
    total_events: int
    alert_events: int
    warning_events: int
    normal_events: int
    offline_events: int
    last_alert: Optional[datetime] = None
    last_maintenance: Optional[datetime] = None
    avg_gas_level: Optional[float] = None
    max_gas_level: Optional[int] = None
    min_battery_level: Optional[int] = None

    # Location hierarchy
    location_type: Optional[str] = None
    apartment_number: Optional[str] = None
    building_name: Optional[str] = None
    client_name: Optional[str] = None
    building_admin: Optional[str] = None  # If exists

    model_config = ConfigDict(from_attributes=True)
