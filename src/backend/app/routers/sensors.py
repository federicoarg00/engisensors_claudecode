"""
Sensor API Router

Endpoints for managing gas sensors.
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.sensor import Sensor, SensorStatus
from app.models.location import Location
from app.models.apartment import Apartment
from app.models.building import Building
from app.models.client import Client
from app.schemas.sensor import (
    SensorCreate,
    SensorUpdate,
    SensorResponse,
    SensorWithLocation,
    SensorStatusUpdate,
)

router = APIRouter(prefix="/api/v1/sensors", tags=["Sensors"])


@router.post(
    "/",
    response_model=SensorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new sensor",
)
async def create_sensor(
    sensor_data: SensorCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new gas sensor in the system.

    - **device_id**: Unique identifier for the sensor (e.g., "S-TC-203-001")
    - **location_id**: UUID of the location where sensor will be installed
    - **model**: Sensor model name (optional)
    - **firmware_version**: Current firmware version (optional)
    - **gas_threshold_ppm**: Alert threshold in PPM (default: 800)
    """
    # Check if device_id already exists
    result = await db.execute(
        select(Sensor).where(Sensor.device_id == sensor_data.device_id)
    )
    existing_sensor = result.scalar_one_or_none()

    if existing_sensor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Sensor with device_id '{sensor_data.device_id}' already exists",
        )

    # Verify location exists
    location_result = await db.execute(
        select(Location).where(Location.id == sensor_data.location_id)
    )
    location = location_result.scalar_one_or_none()

    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id '{sensor_data.location_id}' not found",
        )

    # Create sensor
    new_sensor = Sensor(
        device_id=sensor_data.device_id,
        model=sensor_data.model,
        firmware_version=sensor_data.firmware_version,
        gas_threshold_ppm=sensor_data.gas_threshold_ppm,
        location_id=sensor_data.location_id,
        status=SensorStatus.INACTIVE,  # Start as inactive until first message
    )

    db.add(new_sensor)
    await db.commit()
    await db.refresh(new_sensor)

    return new_sensor


@router.get(
    "/",
    response_model=List[SensorWithLocation],
    summary="List all sensors",
)
async def list_sensors(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    status: Optional[SensorStatus] = Query(None, description="Filter by sensor status"),
    client_id: Optional[UUID] = Query(None, description="Filter by client ID"),
    building_id: Optional[UUID] = Query(None, description="Filter by building ID"),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve a list of all sensors with their location hierarchy.

    Supports filtering by status, client, or building.
    """
    # Build query with joins for full hierarchy
    query = select(Sensor).options(
        selectinload(Sensor.location)
        .selectinload(Location.apartment)
        .selectinload(Apartment.building)
        .selectinload(Building.client)
    )

    # Apply filters
    if status:
        query = query.where(Sensor.status == status)

    if client_id:
        query = query.join(Sensor.location).join(Location.apartment).join(
            Apartment.building
        ).where(Building.client_id == client_id)

    if building_id:
        query = query.join(Sensor.location).join(Location.apartment).where(
            Apartment.building_id == building_id
        )

    # Add pagination
    query = query.offset(skip).limit(limit).order_by(Sensor.created_at.desc())

    result = await db.execute(query)
    sensors = result.scalars().all()

    # Format response with hierarchy
    response = []
    for sensor in sensors:
        sensor_dict = SensorResponse.model_validate(sensor).model_dump()

        # Add location hierarchy
        if sensor.location:
            sensor_dict["location"] = {
                "id": str(sensor.location.id),
                "type": sensor.location.type.value,
                "description": sensor.location.description,
            }

            if sensor.location.apartment:
                sensor_dict["apartment"] = {
                    "id": str(sensor.location.apartment.id),
                    "number": sensor.location.apartment.number,
                    "floor": sensor.location.apartment.floor,
                }

                if sensor.location.apartment.building:
                    sensor_dict["building"] = {
                        "id": str(sensor.location.apartment.building.id),
                        "name": sensor.location.apartment.building.name,
                        "address": sensor.location.apartment.building.address,
                    }

                    if sensor.location.apartment.building.client:
                        sensor_dict["client"] = {
                            "id": str(sensor.location.apartment.building.client.id),
                            "name": sensor.location.apartment.building.client.name,
                            "company": sensor.location.apartment.building.client.company,
                        }

        response.append(sensor_dict)

    return response


@router.get(
    "/{sensor_id}",
    response_model=SensorWithLocation,
    summary="Get sensor by ID",
)
async def get_sensor(
    sensor_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve detailed information about a specific sensor.

    Returns sensor data including full location hierarchy.
    """
    result = await db.execute(
        select(Sensor)
        .where(Sensor.id == sensor_id)
        .options(
            selectinload(Sensor.location)
            .selectinload(Location.apartment)
            .selectinload(Apartment.building)
            .selectinload(Building.client)
        )
    )
    sensor = result.scalar_one_or_none()

    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor with id '{sensor_id}' not found",
        )

    # Format response with hierarchy
    sensor_dict = SensorResponse.model_validate(sensor).model_dump()

    if sensor.location:
        sensor_dict["location"] = {
            "id": str(sensor.location.id),
            "type": sensor.location.type.value,
            "description": sensor.location.description,
        }

        if sensor.location.apartment:
            sensor_dict["apartment"] = {
                "id": str(sensor.location.apartment.id),
                "number": sensor.location.apartment.number,
                "floor": sensor.location.apartment.floor,
            }

            if sensor.location.apartment.building:
                sensor_dict["building"] = {
                    "id": str(sensor.location.apartment.building.id),
                    "name": sensor.location.apartment.building.name,
                    "address": sensor.location.apartment.building.address,
                }

                if sensor.location.apartment.building.client:
                    sensor_dict["client"] = {
                        "id": str(sensor.location.apartment.building.client.id),
                        "name": sensor.location.apartment.building.client.name,
                        "company": sensor.location.apartment.building.client.company,
                    }

    return sensor_dict


@router.get(
    "/device/{device_id}",
    response_model=SensorWithLocation,
    summary="Get sensor by device ID",
)
async def get_sensor_by_device_id(
    device_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve sensor information by device_id.

    Useful for MQTT handler to lookup sensors.
    """
    result = await db.execute(
        select(Sensor)
        .where(Sensor.device_id == device_id)
        .options(
            selectinload(Sensor.location)
            .selectinload(Location.apartment)
            .selectinload(Apartment.building)
            .selectinload(Building.client)
        )
    )
    sensor = result.scalar_one_or_none()

    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor with device_id '{device_id}' not found",
        )

    # Format response (same as get_sensor)
    sensor_dict = SensorResponse.model_validate(sensor).model_dump()

    if sensor.location:
        sensor_dict["location"] = {
            "id": str(sensor.location.id),
            "type": sensor.location.type.value,
            "description": sensor.location.description,
        }

        if sensor.location.apartment:
            sensor_dict["apartment"] = {
                "id": str(sensor.location.apartment.id),
                "number": sensor.location.apartment.number,
                "floor": sensor.location.apartment.floor,
            }

            if sensor.location.apartment.building:
                sensor_dict["building"] = {
                    "id": str(sensor.location.apartment.building.id),
                    "name": sensor.location.apartment.building.name,
                    "address": sensor.location.apartment.building.address,
                }

                if sensor.location.apartment.building.client:
                    sensor_dict["client"] = {
                        "id": str(sensor.location.apartment.building.client.id),
                        "name": sensor.location.apartment.building.client.name,
                        "company": sensor.location.apartment.building.client.company,
                    }

    return sensor_dict


@router.patch(
    "/{sensor_id}",
    response_model=SensorResponse,
    summary="Update sensor",
)
async def update_sensor(
    sensor_id: UUID,
    sensor_update: SensorUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update sensor information.

    Can update model, firmware version, threshold, status, or location.
    """
    result = await db.execute(select(Sensor).where(Sensor.id == sensor_id))
    sensor = result.scalar_one_or_none()

    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor with id '{sensor_id}' not found",
        )

    # Update fields
    update_data = sensor_update.model_dump(exclude_unset=True)

    # If location_id is being updated, verify it exists
    if "location_id" in update_data:
        location_result = await db.execute(
            select(Location).where(Location.id == update_data["location_id"])
        )
        location = location_result.scalar_one_or_none()

        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Location with id '{update_data['location_id']}' not found",
            )

    for key, value in update_data.items():
        setattr(sensor, key, value)

    await db.commit()
    await db.refresh(sensor)

    return sensor


@router.patch(
    "/{sensor_id}/status",
    response_model=SensorResponse,
    summary="Update sensor status",
)
async def update_sensor_status(
    sensor_id: UUID,
    status_update: SensorStatusUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update sensor status, battery level, and signal strength.

    Used for periodic status updates from sensors.
    """
    result = await db.execute(select(Sensor).where(Sensor.id == sensor_id))
    sensor = result.scalar_one_or_none()

    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor with id '{sensor_id}' not found",
        )

    sensor.status = status_update.status

    if status_update.battery_level is not None:
        sensor.battery_level = status_update.battery_level

    if status_update.signal_strength is not None:
        sensor.signal_strength = status_update.signal_strength

    await db.commit()
    await db.refresh(sensor)

    return sensor


@router.delete(
    "/{sensor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete sensor",
)
async def delete_sensor(
    sensor_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a sensor from the system.

    This will also delete all associated sensor events (CASCADE).
    """
    result = await db.execute(select(Sensor).where(Sensor.id == sensor_id))
    sensor = result.scalar_one_or_none()

    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor with id '{sensor_id}' not found",
        )

    await db.delete(sensor)
    await db.commit()

    return None
