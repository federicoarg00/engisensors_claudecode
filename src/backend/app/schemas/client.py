"""
Client Pydantic Schemas

Request/response models for client endpoints.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class ClientBase(BaseModel):
    """Base client schema with common fields."""
    name: str = Field(..., min_length=1, max_length=255, description="Client name or contact person")
    company: Optional[str] = Field(None, max_length=255, description="Company name")
    email: Optional[EmailStr] = Field(None, description="Client email")
    phone: Optional[str] = Field(None, max_length=50, description="Client phone number")
    address: Optional[str] = Field(None, description="Client address")


class ClientCreate(ClientBase):
    """Schema for creating a new client."""
    user_id: Optional[UUID] = Field(None, description="Associated user account ID (optional)")


class ClientUpdate(BaseModel):
    """Schema for updating client information."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    company: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = None
    is_active: Optional[bool] = None
    user_id: Optional[UUID] = None


class ClientResponse(ClientBase):
    """Schema for client response."""
    id: UUID
    is_active: bool
    user_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ClientWithStats(ClientResponse):
    """Schema for client with statistics."""
    total_buildings: int = 0
    total_sensors: int = 0
    active_sensors: int = 0
    alert_sensors: int = 0

    model_config = ConfigDict(from_attributes=True)
