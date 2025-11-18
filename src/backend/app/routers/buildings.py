"""
Buildings API Router

CRUD endpoints for building management and sensor listing.
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.building import Building
from app.models.apartment import Apartment
from app.models.location import Location
from app.models.sensor import Sensor, SensorStatus
from app.models.client import Client
from app.models.user import User
from app.schemas.building import (
    BuildingCreate,
    BuildingUpdate,
    BuildingResponse,
    BuildingWithStats,
    BuildingWithSensors,
    ApartmentSensorInfo,
    SensorWithComputedStatus,
)
from app.utils.sensor_utils import get_computed_sensor_status

router = APIRouter(prefix="/api/v1/buildings", tags=["Buildings"])


@router.get(
    "",
    response_model=List[BuildingWithStats],
    summary="List all buildings with statistics",
)
async def list_buildings(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    client_id: Optional[UUID] = Query(None, description="Filter by client ID"),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve all buildings with sensor statistics.

    Returns buildings with counts for each sensor category:
    - total_sensors: Total installed sensors
    - online_sensors: Operational sensors
    - failure_sensors: Sensors with technical issues
    - alert_sensors: Sensors detecting gas
    - disconnected_sensors: Sensors that haven't reported
    """
    # Build query
    query = (
        select(Building)
        .where(Building.deleted_at.is_(None))
        .options(
            selectinload(Building.client),
            selectinload(Building.admin),
            selectinload(Building.apartments)
            .selectinload(Apartment.locations)
            .selectinload(Location.sensors)
        )
    )

    if client_id:
        query = query.where(Building.client_id == client_id)

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    buildings = result.scalars().all()

    # Calculate statistics for each building
    response = []
    for building in buildings:
        # Collect all sensors for this building
        sensors = []
        for apartment in building.apartments:
            if apartment.deleted_at:
                continue
            for location in apartment.locations:
                if location.deleted_at:
                    continue
                for sensor in location.sensors:
                    if sensor.deleted_at:
                        continue
                    sensors.append(sensor)

        # Calculate 5 sensor categories using computed status
        total_sensors = len(sensors)
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

        building_data = BuildingWithStats(
            id=building.id,
            client_id=building.client_id,
            admin_id=building.admin_id,
            name=building.name,
            address=building.address,
            city=building.city,
            state=building.state,
            country=building.country,
            postal_code=building.postal_code,
            latitude=building.latitude,
            longitude=building.longitude,
            created_at=building.created_at,
            updated_at=building.updated_at,
            client_name=building.client.name if building.client else None,
            admin_name=building.admin.email.split('@')[0] if building.admin else None,
            admin_email=building.admin.email if building.admin else None,
            total_apartments=len([a for a in building.apartments if not a.deleted_at]),
            total_sensors=total_sensors,
            online_sensors=online_count,
            failure_sensors=failure_count,
            alert_sensors=alert_count,
            disconnected_sensors=disconnected_count,
        )

        response.append(building_data)

    return response


@router.get(
    "/{building_id}",
    response_model=BuildingWithStats,
    summary="Get building by ID",
)
async def get_building(
    building_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve a specific building by ID with sensor statistics.
    """
    result = await db.execute(
        select(Building)
        .where(and_(Building.id == building_id, Building.deleted_at.is_(None)))
        .options(
            selectinload(Building.client),
            selectinload(Building.admin),
            selectinload(Building.apartments)
            .selectinload(Apartment.locations)
            .selectinload(Location.sensors)
        )
    )
    building = result.scalar_one_or_none()

    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Building with id '{building_id}' not found",
        )

    # Collect all sensors
    sensors = []
    for apartment in building.apartments:
        if apartment.deleted_at:
            continue
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

    return BuildingWithStats(
        id=building.id,
        client_id=building.client_id,
        admin_id=building.admin_id,
        name=building.name,
        address=building.address,
        city=building.city,
        state=building.state,
        country=building.country,
        postal_code=building.postal_code,
        latitude=building.latitude,
        longitude=building.longitude,
        created_at=building.created_at,
        updated_at=building.updated_at,
        client_name=building.client.name if building.client else None,
        admin_name=building.admin.email.split('@')[0] if building.admin else None,
        admin_email=building.admin.email if building.admin else None,
        total_apartments=len([a for a in building.apartments if not a.deleted_at]),
        total_sensors=len(sensors),
        online_sensors=online_count,
        failure_sensors=failure_count,
        alert_sensors=alert_count,
        disconnected_sensors=disconnected_count,
    )


@router.get(
    "/{building_id}/sensors",
    response_model=BuildingWithSensors,
    summary="Get all sensors for a building",
)
async def get_building_sensors(
    building_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve all sensors for a building organized by apartment.

    Returns sensors with computed status based on:
    - Disconnection timeout (default 6 hours without heartbeat)
    - Alert status (gas detection)
    - Failure status (maintenance, low battery)
    - Online status (operational)

    Each sensor includes:
    - Device info (ID, model, firmware)
    - Battery level and signal strength
    - Last seen timestamp
    - Computed status category and description
    - Location type (cocina, lavadero, etc.)
    """
    result = await db.execute(
        select(Building)
        .where(and_(Building.id == building_id, Building.deleted_at.is_(None)))
        .options(
            selectinload(Building.client),
            selectinload(Building.apartments)
            .selectinload(Apartment.locations)
            .selectinload(Location.sensors)
        )
    )
    building = result.scalar_one_or_none()

    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Building with id '{building_id}' not found",
        )

    # Build apartment sensor structure
    apartments_data = []
    total_sensors = 0
    online_count = 0
    failure_count = 0
    alert_count = 0
    disconnected_count = 0

    for apartment in sorted(building.apartments, key=lambda a: a.number):
        if apartment.deleted_at:
            continue

        apartment_sensors = []

        for location in apartment.locations:
            if location.deleted_at:
                continue

            for sensor in location.sensors:
                if sensor.deleted_at:
                    continue

                # Get computed status
                status_desc, category = get_computed_sensor_status(sensor)

                # Count by category
                total_sensors += 1
                if category == "online":
                    online_count += 1
                elif category == "failure":
                    failure_count += 1
                elif category == "alert":
                    alert_count += 1
                elif category == "disconnected":
                    disconnected_count += 1

                sensor_data = SensorWithComputedStatus(
                    id=sensor.id,
                    device_id=sensor.device_id,
                    model=sensor.model,
                    firmware_version=sensor.firmware_version,
                    gas_threshold_ppm=sensor.gas_threshold_ppm,
                    battery_level=sensor.battery_level,
                    signal_strength=sensor.signal_strength,
                    last_seen=sensor.last_seen,
                    location_id=location.id,
                    location_type=location.location_type.value,
                    status_category=category,
                    status_description=status_desc,
                    db_status=sensor.status.value,
                    created_at=sensor.created_at,
                    updated_at=sensor.updated_at,
                )
                apartment_sensors.append(sensor_data)

        if apartment_sensors:  # Only include apartments that have sensors
            apartment_info = ApartmentSensorInfo(
                apartment_id=apartment.id,
                apartment_number=apartment.number,
                floor=apartment.floor,
                sensors=apartment_sensors,
            )
            apartments_data.append(apartment_info)

    return BuildingWithSensors(
        id=building.id,
        client_id=building.client_id,
        name=building.name,
        address=building.address,
        city=building.city,
        state=building.state,
        country=building.country,
        postal_code=building.postal_code,
        latitude=building.latitude,
        longitude=building.longitude,
        created_at=building.created_at,
        updated_at=building.updated_at,
        client_name=building.client.name if building.client else None,
        apartments=apartments_data,
        total_sensors=total_sensors,
        online_sensors=online_count,
        failure_sensors=failure_count,
        alert_sensors=alert_count,
        disconnected_sensors=disconnected_count,
    )


@router.post(
    "",
    response_model=BuildingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new building",
)
async def create_building(
    building_data: BuildingCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new building for a client.
    """
    # Verify client exists
    client_result = await db.execute(
        select(Client).where(
            and_(Client.id == building_data.client_id, Client.deleted_at.is_(None))
        )
    )
    client = client_result.scalar_one_or_none()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with id '{building_data.client_id}' not found",
        )

    # Verify admin exists if provided
    if building_data.admin_id:
        admin_result = await db.execute(
            select(User).where(User.id == building_data.admin_id)
        )
        admin = admin_result.scalar_one_or_none()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id '{building_data.admin_id}' not found",
            )

    # Create building
    building = Building(
        client_id=building_data.client_id,
        admin_id=building_data.admin_id,
        name=building_data.name,
        address=building_data.address,
        city=building_data.city,
        state=building_data.state,
        country=building_data.country,
        postal_code=building_data.postal_code,
        latitude=building_data.latitude,
        longitude=building_data.longitude,
    )

    db.add(building)
    await db.commit()
    await db.refresh(building)

    return building


@router.patch(
    "/{building_id}",
    response_model=BuildingResponse,
    summary="Update a building",
)
async def update_building(
    building_id: UUID,
    building_data: BuildingUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an existing building's information.
    """
    result = await db.execute(
        select(Building).where(
            and_(Building.id == building_id, Building.deleted_at.is_(None))
        )
    )
    building = result.scalar_one_or_none()

    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Building with id '{building_id}' not found",
        )

    # Update fields
    update_data = building_data.model_dump(exclude_unset=True)

    # Verify admin exists if being updated
    if "admin_id" in update_data and update_data["admin_id"]:
        admin_result = await db.execute(
            select(User).where(User.id == update_data["admin_id"])
        )
        admin = admin_result.scalar_one_or_none()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id '{update_data['admin_id']}' not found",
            )

    for field, value in update_data.items():
        setattr(building, field, value)

    await db.commit()
    await db.refresh(building)

    return building


@router.delete(
    "/{building_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a building",
)
async def delete_building(
    building_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Soft delete a building and all its apartments, locations, and sensors.
    """
    from datetime import datetime

    result = await db.execute(
        select(Building).where(
            and_(Building.id == building_id, Building.deleted_at.is_(None))
        )
    )
    building = result.scalar_one_or_none()

    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Building with id '{building_id}' not found",
        )

    # Soft delete
    building.deleted_at = datetime.utcnow()
    await db.commit()

    return None
