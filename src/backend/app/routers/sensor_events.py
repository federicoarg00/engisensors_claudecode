"""
Sensor Events API Router

Endpoints for querying sensor events and statistics.
"""
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.config import settings
from app.models.sensor import Sensor
from app.models.sensor_event import SensorEvent, EventType
from app.models.location import Location
from app.models.apartment import Apartment
from app.models.building import Building
from app.models.client import Client
from app.schemas.sensor_event import (
    SensorEventResponse,
    SensorEventWithLocation,
    SensorStatsResponse,
)

router = APIRouter(prefix="/api/v1/sensor-events", tags=["Sensor Events"])


@router.get(
    "/sensor/{sensor_id}",
    response_model=List[SensorEventWithLocation],
    summary="Get events for a specific sensor",
)
async def get_sensor_events(
    sensor_id: UUID,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    event_type: Optional[EventType] = Query(None, description="Filter by event type"),
    start_date: Optional[datetime] = Query(None, description="Filter events after this date"),
    end_date: Optional[datetime] = Query(None, description="Filter events before this date"),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve historical events for a specific sensor.

    Returns events in reverse chronological order (newest first).
    Supports filtering by event type and date range.
    """
    # Verify sensor exists and get location hierarchy
    sensor_result = await db.execute(
        select(Sensor)
        .where(Sensor.id == sensor_id)
        .options(
            selectinload(Sensor.location)
            .selectinload(Location.apartment)
            .selectinload(Apartment.building)
            .selectinload(Building.client)
        )
    )
    sensor = sensor_result.scalar_one_or_none()

    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor with id '{sensor_id}' not found",
        )

    # Build query with filters
    query = select(SensorEvent).where(SensorEvent.sensor_id == sensor_id)

    if event_type:
        query = query.where(SensorEvent.event_type == event_type)

    if start_date:
        query = query.where(SensorEvent.timestamp >= start_date)

    if end_date:
        query = query.where(SensorEvent.timestamp <= end_date)

    # Order by timestamp descending (newest first)
    query = query.order_by(desc(SensorEvent.timestamp))

    # Add pagination
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    events = result.scalars().all()

    # Format response with location info
    response = []
    for event in events:
        event_dict = SensorEventResponse.model_validate(event).model_dump()

        # Add sensor and location hierarchy
        event_dict["sensor_device_id"] = sensor.device_id
        if sensor.location:
            event_dict["location_type"] = sensor.location.type.value
            if sensor.location.apartment:
                event_dict["apartment_number"] = sensor.location.apartment.number
                if sensor.location.apartment.building:
                    event_dict["building_name"] = sensor.location.apartment.building.name
                    if sensor.location.apartment.building.client:
                        event_dict["client_name"] = sensor.location.apartment.building.client.name

        response.append(event_dict)

    return response


@router.get(
    "/sensor/{sensor_id}/stats",
    response_model=SensorStatsResponse,
    summary="Get statistics for a specific sensor",
)
async def get_sensor_stats(
    sensor_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve comprehensive statistics and metadata for a sensor.

    Returns:
    - Sensor metadata (activation date, days active, current status)
    - Event statistics (total, by type, last alert)
    - Gas level statistics (avg, max)
    - Battery statistics (min level)
    - Location hierarchy (client, building, apartment, location)
    - Building admin if exists
    """
    # Get sensor with full hierarchy
    sensor_result = await db.execute(
        select(Sensor)
        .where(Sensor.id == sensor_id)
        .options(
            selectinload(Sensor.location)
            .selectinload(Location.apartment)
            .selectinload(Apartment.building)
            .selectinload(Building.client)
            .selectinload(Client.user)
        )
    )
    sensor = sensor_result.scalar_one_or_none()

    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor with id '{sensor_id}' not found",
        )

    # Calculate days active
    days_active = (datetime.utcnow() - sensor.created_at).days

    # Get event statistics
    total_events_result = await db.execute(
        select(func.count(SensorEvent.id)).where(SensorEvent.sensor_id == sensor_id)
    )
    total_events = total_events_result.scalar() or 0

    # Count by event type
    alert_events_result = await db.execute(
        select(func.count(SensorEvent.id)).where(
            and_(SensorEvent.sensor_id == sensor_id, SensorEvent.event_type == EventType.ALERT)
        )
    )
    alert_events = alert_events_result.scalar() or 0

    warning_events_result = await db.execute(
        select(func.count(SensorEvent.id)).where(
            and_(SensorEvent.sensor_id == sensor_id, SensorEvent.event_type == EventType.WARNING)
        )
    )
    warning_events = warning_events_result.scalar() or 0

    normal_events_result = await db.execute(
        select(func.count(SensorEvent.id)).where(
            and_(SensorEvent.sensor_id == sensor_id, SensorEvent.event_type == EventType.NORMAL)
        )
    )
    normal_events = normal_events_result.scalar() or 0

    offline_events_result = await db.execute(
        select(func.count(SensorEvent.id)).where(
            and_(SensorEvent.sensor_id == sensor_id, SensorEvent.event_type == EventType.OFFLINE)
        )
    )
    offline_events = offline_events_result.scalar() or 0

    # Get last alert timestamp
    last_alert_result = await db.execute(
        select(SensorEvent.timestamp)
        .where(and_(SensorEvent.sensor_id == sensor_id, SensorEvent.event_type == EventType.ALERT))
        .order_by(desc(SensorEvent.timestamp))
        .limit(1)
    )
    last_alert = last_alert_result.scalar_one_or_none()

    # Get gas level statistics
    gas_stats_result = await db.execute(
        select(
            func.avg(SensorEvent.gas_level).label("avg_gas"),
            func.max(SensorEvent.gas_level).label("max_gas"),
        ).where(and_(SensorEvent.sensor_id == sensor_id, SensorEvent.gas_level.isnot(None)))
    )
    gas_stats = gas_stats_result.one_or_none()
    avg_gas_level = round(gas_stats[0], 2) if gas_stats and gas_stats[0] else None
    max_gas_level = gas_stats[1] if gas_stats else None

    # Get minimum battery level
    min_battery_result = await db.execute(
        select(func.min(SensorEvent.battery_level)).where(
            and_(SensorEvent.sensor_id == sensor_id, SensorEvent.battery_level.isnot(None))
        )
    )
    min_battery_level = min_battery_result.scalar_one_or_none()

    # Build response with location hierarchy
    stats = {
        "sensor_id": sensor.id,
        "device_id": sensor.device_id,
        "activation_date": sensor.created_at,
        "days_active": days_active,
        "current_status": sensor.status.value,
        "total_events": total_events,
        "alert_events": alert_events,
        "warning_events": warning_events,
        "normal_events": normal_events,
        "offline_events": offline_events,
        "last_alert": last_alert,
        "last_maintenance": None,  # TODO: Add maintenance tracking
        "avg_gas_level": avg_gas_level,
        "max_gas_level": max_gas_level,
        "min_battery_level": min_battery_level,
    }

    # Add location hierarchy
    if sensor.location:
        stats["location_type"] = sensor.location.type.value
        if sensor.location.apartment:
            stats["apartment_number"] = sensor.location.apartment.number
            if sensor.location.apartment.building:
                stats["building_name"] = sensor.location.apartment.building.name
                if sensor.location.apartment.building.client:
                    stats["client_name"] = sensor.location.apartment.building.client.name
                    # Check if client has a user (building admin)
                    if sensor.location.apartment.building.client.user:
                        stats["building_admin"] = sensor.location.apartment.building.client.user.full_name

    return stats


@router.get(
    "/recent",
    response_model=List[SensorEventWithLocation],
    summary="Get recent events across all sensors",
)
async def get_recent_events(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=500, description="Maximum number of records to return"),
    event_type: Optional[EventType] = Query(None, description="Filter by event type"),
    client_id: Optional[UUID] = Query(None, description="Filter by client ID"),
    hours: int = Query(24, ge=1, le=168, description="Get events from last N hours (default: 24)"),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve recent events across all sensors.

    Useful for dashboard displays showing recent alerts and activity.
    Returns events in reverse chronological order (newest first).
    """
    # Calculate time threshold
    time_threshold = datetime.utcnow() - timedelta(hours=hours)

    # Build base query
    query = (
        select(SensorEvent, Sensor)
        .join(Sensor, Sensor.id == SensorEvent.sensor_id)
        .where(SensorEvent.timestamp >= time_threshold)
    )

    # Apply filters
    if event_type:
        query = query.where(SensorEvent.event_type == event_type)

    if client_id:
        query = (
            query.join(Location, Location.id == Sensor.location_id)
            .join(Apartment, Apartment.id == Location.apartment_id)
            .join(Building, Building.id == Apartment.building_id)
            .where(Building.client_id == client_id)
        )

    # Order by timestamp descending
    query = query.order_by(desc(SensorEvent.timestamp))

    # Add pagination
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    events_with_sensors = result.all()

    # Format response with location info
    response = []
    for event, sensor in events_with_sensors:
        # Load location hierarchy if not already loaded
        if not sensor.location:
            await db.refresh(
                sensor,
                ["location"],
            )

        event_dict = SensorEventResponse.model_validate(event).model_dump()

        # Add sensor and location hierarchy
        event_dict["sensor_device_id"] = sensor.device_id
        if sensor.location:
            event_dict["location_type"] = sensor.location.type.value
            if sensor.location.apartment:
                event_dict["apartment_number"] = sensor.location.apartment.number
                if sensor.location.apartment.building:
                    event_dict["building_name"] = sensor.location.apartment.building.name
                    if sensor.location.apartment.building.client:
                        event_dict["client_name"] = sensor.location.apartment.building.client.name

        response.append(event_dict)

    return response
