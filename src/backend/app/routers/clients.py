"""
Client API Router

Endpoints for managing clients.
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.client import Client
from app.models.building import Building
from app.models.sensor import Sensor, SensorStatus
from app.models.apartment import Apartment
from app.models.location import Location
from app.schemas.client import (
    ClientCreate,
    ClientUpdate,
    ClientResponse,
    ClientWithStats,
)

router = APIRouter(prefix="/api/v1/clients", tags=["Clients"])


@router.post(
    "/",
    response_model=ClientResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new client",
)
async def create_client(
    client_data: ClientCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new client in the system.

    - **name**: Client name or contact person
    - **company**: Company name (optional)
    - **email**: Client email (optional)
    - **phone**: Client phone number (optional)
    - **address**: Client address (optional)
    - **user_id**: Associated user account ID (optional)
    """
    new_client = Client(
        name=client_data.name,
        company=client_data.company,
        email=client_data.email,
        phone=client_data.phone,
        address=client_data.address,
        user_id=client_data.user_id,
    )

    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)

    return new_client


@router.get(
    "/",
    response_model=List[ClientWithStats],
    summary="List all clients",
)
async def list_clients(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    is_active: bool = Query(None, description="Filter by active status"),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve a list of all clients with statistics.

    Returns total buildings, total sensors, active sensors, and alert sensors for each client.
    """
    # Build query
    query = select(Client).order_by(Client.created_at.desc())

    # Apply filters
    if is_active is not None:
        query = query.where(Client.is_active == is_active)

    # Add pagination
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    clients = result.scalars().all()

    # Fetch statistics for each client
    response = []
    for client in clients:
        client_dict = ClientResponse.model_validate(client).model_dump()

        # Count buildings
        buildings_result = await db.execute(
            select(func.count(Building.id)).where(Building.client_id == client.id)
        )
        total_buildings = buildings_result.scalar() or 0

        # Count sensors through the hierarchy
        sensors_query = (
            select(Sensor, Sensor.status)
            .join(Location, Location.id == Sensor.location_id)
            .join(Apartment, Apartment.id == Location.apartment_id)
            .join(Building, Building.id == Apartment.building_id)
            .where(Building.client_id == client.id)
        )

        sensors_result = await db.execute(sensors_query)
        sensors = sensors_result.all()

        total_sensors = len(sensors)
        active_sensors = sum(1 for _, status in sensors if status == SensorStatus.ACTIVE)
        alert_sensors = sum(1 for _, status in sensors if status == SensorStatus.ALERT)

        client_dict["total_buildings"] = total_buildings
        client_dict["total_sensors"] = total_sensors
        client_dict["active_sensors"] = active_sensors
        client_dict["alert_sensors"] = alert_sensors

        response.append(client_dict)

    return response


@router.get(
    "/{client_id}",
    response_model=ClientWithStats,
    summary="Get client by ID",
)
async def get_client(
    client_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve detailed information about a specific client.

    Returns client data including statistics.
    """
    result = await db.execute(select(Client).where(Client.id == client_id))
    client = result.scalar_one_or_none()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with id '{client_id}' not found",
        )

    client_dict = ClientResponse.model_validate(client).model_dump()

    # Count buildings
    buildings_result = await db.execute(
        select(func.count(Building.id)).where(Building.client_id == client.id)
    )
    total_buildings = buildings_result.scalar() or 0

    # Count sensors
    sensors_query = (
        select(Sensor, Sensor.status)
        .join(Location, Location.id == Sensor.location_id)
        .join(Apartment, Apartment.id == Location.apartment_id)
        .join(Building, Building.id == Apartment.building_id)
        .where(Building.client_id == client.id)
    )

    sensors_result = await db.execute(sensors_query)
    sensors = sensors_result.all()

    total_sensors = len(sensors)
    active_sensors = sum(1 for _, status in sensors if status == SensorStatus.ACTIVE)
    alert_sensors = sum(1 for _, status in sensors if status == SensorStatus.ALERT)

    client_dict["total_buildings"] = total_buildings
    client_dict["total_sensors"] = total_sensors
    client_dict["active_sensors"] = active_sensors
    client_dict["alert_sensors"] = alert_sensors

    return client_dict


@router.patch(
    "/{client_id}",
    response_model=ClientResponse,
    summary="Update client",
)
async def update_client(
    client_id: UUID,
    client_update: ClientUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update client information.

    Can update any client field except ID.
    """
    result = await db.execute(select(Client).where(Client.id == client_id))
    client = result.scalar_one_or_none()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with id '{client_id}' not found",
        )

    # Update fields
    update_data = client_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(client, key, value)

    await db.commit()
    await db.refresh(client)

    return client


@router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete client",
)
async def delete_client(
    client_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a client from the system.

    This will also delete all associated buildings, apartments, locations, sensors, and events (CASCADE).
    Use with caution!
    """
    result = await db.execute(select(Client).where(Client.id == client_id))
    client = result.scalar_one_or_none()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with id '{client_id}' not found",
        )

    await db.delete(client)
    await db.commit()

    return None
