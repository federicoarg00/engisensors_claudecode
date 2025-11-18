"""
Locations API Router

CRUD endpoints for location management.
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.location import Location
from app.models.apartment import Apartment
from app.models.building import Building
from app.models.sensor import Sensor
from app.schemas.location import (
    LocationCreate,
    LocationUpdate,
    LocationResponse,
    LocationWithSensor,
)
from app.utils.sensor_utils import get_computed_sensor_status

router = APIRouter(prefix="/api/v1/locations", tags=["Locations"])


@router.get(
    "",
    response_model=List[LocationWithSensor],
    summary="List all locations with sensor info",
)
async def list_locations(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    apartment_id: Optional[UUID] = Query(None, description="Filter by apartment ID"),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve all locations with sensor information.
    """
    query = (
        select(Location)
        .where(Location.deleted_at.is_(None))
        .options(
            selectinload(Location.apartment)
            .selectinload(Apartment.building)
            .selectinload(Building.client),
            selectinload(Location.sensors)
        )
    )

    if apartment_id:
        query = query.where(Location.apartment_id == apartment_id)

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    locations = result.scalars().all()

    response = []
    for location in locations:
        # Get first active sensor (a location typically has one sensor)
        active_sensor = None
        for sensor in location.sensors:
            if not sensor.deleted_at:
                active_sensor = sensor
                break

        sensor_status = None
        if active_sensor:
            status_desc, _ = get_computed_sensor_status(active_sensor)
            sensor_status = status_desc

        location_data = LocationWithSensor(
            id=location.id,
            apartment_id=location.apartment_id,
            location_type=location.location_type,
            description=location.description,
            created_at=location.created_at,
            updated_at=location.updated_at,
            apartment_number=location.apartment.number if location.apartment else None,
            building_name=location.apartment.building.name if location.apartment and location.apartment.building else None,
            client_name=location.apartment.building.client.name if location.apartment and location.apartment.building and location.apartment.building.client else None,
            has_sensor=active_sensor is not None,
            sensor_id=active_sensor.id if active_sensor else None,
            sensor_device_id=active_sensor.device_id if active_sensor else None,
            sensor_status=sensor_status,
        )
        response.append(location_data)

    return response


@router.get(
    "/{location_id}",
    response_model=LocationWithSensor,
    summary="Get location by ID",
)
async def get_location(
    location_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve a specific location by ID with sensor information.
    """
    result = await db.execute(
        select(Location)
        .where(and_(Location.id == location_id, Location.deleted_at.is_(None)))
        .options(
            selectinload(Location.apartment)
            .selectinload(Apartment.building)
            .selectinload(Building.client),
            selectinload(Location.sensors)
        )
    )
    location = result.scalar_one_or_none()

    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id '{location_id}' not found",
        )

    active_sensor = None
    for sensor in location.sensors:
        if not sensor.deleted_at:
            active_sensor = sensor
            break

    sensor_status = None
    if active_sensor:
        status_desc, _ = get_computed_sensor_status(active_sensor)
        sensor_status = status_desc

    return LocationWithSensor(
        id=location.id,
        apartment_id=location.apartment_id,
        location_type=location.location_type,
        description=location.description,
        created_at=location.created_at,
        updated_at=location.updated_at,
        apartment_number=location.apartment.number if location.apartment else None,
        building_name=location.apartment.building.name if location.apartment and location.apartment.building else None,
        client_name=location.apartment.building.client.name if location.apartment and location.apartment.building and location.apartment.building.client else None,
        has_sensor=active_sensor is not None,
        sensor_id=active_sensor.id if active_sensor else None,
        sensor_device_id=active_sensor.device_id if active_sensor else None,
        sensor_status=sensor_status,
    )


@router.post(
    "",
    response_model=LocationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new location",
)
async def create_location(
    location_data: LocationCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new location in an apartment.
    """
    # Verify apartment exists
    apartment_result = await db.execute(
        select(Apartment).where(
            and_(Apartment.id == location_data.apartment_id, Apartment.deleted_at.is_(None))
        )
    )
    apartment = apartment_result.scalar_one_or_none()

    if not apartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Apartment with id '{location_data.apartment_id}' not found",
        )

    location = Location(
        apartment_id=location_data.apartment_id,
        location_type=location_data.location_type,
        description=location_data.description,
    )

    db.add(location)
    await db.commit()
    await db.refresh(location)

    return location


@router.patch(
    "/{location_id}",
    response_model=LocationResponse,
    summary="Update a location",
)
async def update_location(
    location_id: UUID,
    location_data: LocationUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an existing location's information.
    """
    result = await db.execute(
        select(Location).where(
            and_(Location.id == location_id, Location.deleted_at.is_(None))
        )
    )
    location = result.scalar_one_or_none()

    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id '{location_id}' not found",
        )

    update_data = location_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(location, field, value)

    await db.commit()
    await db.refresh(location)

    return location


@router.delete(
    "/{location_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a location",
)
async def delete_location(
    location_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Soft delete a location and its sensors.
    """
    from datetime import datetime

    result = await db.execute(
        select(Location).where(
            and_(Location.id == location_id, Location.deleted_at.is_(None))
        )
    )
    location = result.scalar_one_or_none()

    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id '{location_id}' not found",
        )

    location.deleted_at = datetime.utcnow()
    await db.commit()

    return None
