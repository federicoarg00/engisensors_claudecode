"""
Association Tables for Many-to-Many Relationships

Manages relationships between users and buildings/apartments.
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Boolean, Table
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


# Building Administrators - Many-to-Many between User and Building
building_admins = Table(
    'building_admins',
    Base.metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('building_id', UUID(as_uuid=True), ForeignKey('buildings.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('created_at', DateTime, default=datetime.utcnow, nullable=False),
    Column('created_by', UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
)


# Apartment Owners - Many-to-Many between User and Apartment
apartment_owners = Table(
    'apartment_owners',
    Base.metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('apartment_id', UUID(as_uuid=True), ForeignKey('apartments.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('is_primary', Boolean, default=False, nullable=False),  # Primary owner
    Column('created_at', DateTime, default=datetime.utcnow, nullable=False),
    Column('created_by', UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
)


# Apartment Residents - Many-to-Many between User and Apartment
apartment_residents = Table(
    'apartment_residents',
    Base.metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('apartment_id', UUID(as_uuid=True), ForeignKey('apartments.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('added_by_user_id', UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True),  # Owner who added them
    Column('created_at', DateTime, default=datetime.utcnow, nullable=False),
)
