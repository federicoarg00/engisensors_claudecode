"""
Apartments API Router

CRUD endpoints for apartment management.
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.apartment import Apartment
from app.models.building import Building
from app.models.location import Location
from app.models.sensor import Sensor
from app.schemas.apartment import (
    ApartmentCreate,
    ApartmentUpdate,
    ApartmentResponse,
    ApartmentWithStats,
)
from app.utils.sensor_utils import get_computed_sensor_status

router = APIRouter(prefix="/api/v1/apartments", tags=["Apartments"])


@router.get(
    "",
    response_model=List[ApartmentWithStats],
    summary="List all apartments with statistics",
)
async def list_apartments(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    building_id: Optional[UUID] = Query(None, description="Filter by building ID"),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve all apartments with sensor statistics.
    """
    query = (
        select(Apartment)
        .where(Apartment.deleted_at.is_(None))
        .options(
            selectinload(Apartment.building),
            selectinload(Apartment.locations).selectinload(Location.sensors)
        )
    )

    if building_id:
        query = query.where(Apartment.building_id == building_id)

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    apartments = result.scalars().all()

    response = []
    for apartment in apartments:
        sensors = []
        for location in apartment.locations:
            if location.deleted_at:
                continue
            for sensor in location.sensors:
                if sensor.deleted_at:
                    continue
                sensors.append(sensor)

        # Calculate categories
        online_count = 0
        failure_count = 0
        alert_count = 0
        disconnected_count = 0

        for sensor in sensors:
            _, category = get_computed_sensor_status(sensor)
            if category == "online":
                online_count += 1
            elif category == "failure":
                failure_count += 1
            elif category == "alert":
                alert_count += 1
            elif category == "disconnected":
                disconnected_count += 1

        apartment_data = ApartmentWithStats(
            id=apartment.id,
            building_id=apartment.building_id,
            number=apartment.number,
            floor=apartment.floor,
            description=apartment.description,
            created_at=apartment.created_at,
            updated_at=apartment.updated_at,
            building_name=apartment.building.name if apartment.building else None,
            total_locations=len([l for l in apartment.locations if not l.deleted_at]),
            total_sensors=len(sensors),
            online_sensors=online_count,
            failure_sensors=failure_count,
            alert_sensors=alert_count,
            disconnected_sensors=disconnected_count,
        )
        response.append(apartment_data)

    return response


@router.get(
    "/{apartment_id}",
    response_model=ApartmentWithStats,
    summary="Get apartment by ID",
)
async def get_apartment(
    apartment_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve a specific apartment by ID with sensor statistics.
    """
    result = await db.execute(
        select(Apartment)
        .where(and_(Apartment.id == apartment_id, Apartment.deleted_at.is_(None)))
        .options(
            selectinload(Apartment.building),
            selectinload(Apartment.locations).selectinload(Location.sensors)
        )
    )
    apartment = result.scalar_one_or_none()

    if not apartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Apartment with id '{apartment_id}' not found",
        )

    sensors = []
    for location in apartment.locations:
        if location.deleted_at:
            continue
        for sensor in location.sensors:
            if sensor.deleted_at:
                continue
            sensors.append(sensor)

    online_count = 0
    failure_count = 0
    alert_count = 0
    disconnected_count = 0

    for sensor in sensors:
        _, category = get_computed_sensor_status(sensor)
        if category == "online":
            online_count += 1
        elif category == "failure":
            failure_count += 1
        elif category == "alert":
            alert_count += 1
        elif category == "disconnected":
            disconnected_count += 1

    return ApartmentWithStats(
        id=apartment.id,
        building_id=apartment.building_id,
        number=apartment.number,
        floor=apartment.floor,
        description=apartment.description,
        created_at=apartment.created_at,
        updated_at=apartment.updated_at,
        building_name=apartment.building.name if apartment.building else None,
        total_locations=len([l for l in apartment.locations if not l.deleted_at]),
        total_sensors=len(sensors),
        online_sensors=online_count,
        failure_sensors=failure_count,
        alert_sensors=alert_count,
        disconnected_sensors=disconnected_count,
    )


@router.post(
    "",
    response_model=ApartmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new apartment",
)
async def create_apartment(
    apartment_data: ApartmentCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new apartment in a building.
    """
    # Verify building exists
    building_result = await db.execute(
        select(Building).where(
            and_(Building.id == apartment_data.building_id, Building.deleted_at.is_(None))
        )
    )
    building = building_result.scalar_one_or_none()

    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Building with id '{apartment_data.building_id}' not found",
        )

    # Check for duplicate apartment number in same building
    existing = await db.execute(
        select(Apartment).where(
            and_(
                Apartment.building_id == apartment_data.building_id,
                Apartment.number == apartment_data.number,
                Apartment.deleted_at.is_(None)
            )
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Apartment '{apartment_data.number}' already exists in this building",
        )

    apartment = Apartment(
        building_id=apartment_data.building_id,
        number=apartment_data.number,
        floor=apartment_data.floor,
        description=apartment_data.description,
    )

    db.add(apartment)
    await db.commit()
    await db.refresh(apartment)

    return apartment


@router.patch(
    "/{apartment_id}",
    response_model=ApartmentResponse,
    summary="Update an apartment",
)
async def update_apartment(
    apartment_id: UUID,
    apartment_data: ApartmentUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an existing apartment's information.
    """
    result = await db.execute(
        select(Apartment).where(
            and_(Apartment.id == apartment_id, Apartment.deleted_at.is_(None))
        )
    )
    apartment = result.scalar_one_or_none()

    if not apartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Apartment with id '{apartment_id}' not found",
        )

    update_data = apartment_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(apartment, field, value)

    await db.commit()
    await db.refresh(apartment)

    return apartment


@router.delete(
    "/{apartment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an apartment",
)
async def delete_apartment(
    apartment_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Soft delete an apartment and all its locations and sensors.
    """
    from datetime import datetime

    result = await db.execute(
        select(Apartment).where(
            and_(Apartment.id == apartment_id, Apartment.deleted_at.is_(None))
        )
    )
    apartment = result.scalar_one_or_none()

    if not apartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Apartment with id '{apartment_id}' not found",
        )

    apartment.deleted_at = datetime.utcnow()
    await db.commit()

    return None
