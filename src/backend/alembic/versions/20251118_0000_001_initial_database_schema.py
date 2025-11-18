"""Initial database schema with all models

Revision ID: 001
Revises:
Create Date: 2025-11-18 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create ENUM types
    op.execute("CREATE TYPE userrole AS ENUM ('admin', 'client')")
    op.execute("CREATE TYPE sensorstatus AS ENUM ('active', 'inactive', 'alert', 'maintenance', 'disconnected')")
    op.execute("CREATE TYPE eventtype AS ENUM ('normal', 'alert', 'warning', 'offline', 'online')")
    op.execute("CREATE TYPE locationtype AS ENUM ('cocina', 'lavadero', 'sala', 'recamara', 'bano', 'pasillo', 'estacionamiento', 'bodega', 'oficina', 'otro')")
    op.execute("CREATE TYPE notificationchannel AS ENUM ('email', 'sms')")
    op.execute("CREATE TYPE notificationstatus AS ENUM ('pending', 'sent', 'failed')")

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('role', postgresql.ENUM('admin', 'client', name='userrole'), nullable=False, index=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )

    # Create clients table
    op.create_table(
        'clients',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, index=True),
        sa.Column('company', sa.String(255), nullable=True),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('phone', sa.String(50), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )
    op.create_index('ix_clients_user_id', 'clients', ['user_id'])

    # Create buildings table
    op.create_table(
        'buildings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, index=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('state', sa.String(100), nullable=True),
        sa.Column('country', sa.String(100), nullable=True, server_default='México'),
        sa.Column('postal_code', sa.String(20), nullable=True),
        sa.Column('client_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )
    op.create_index('ix_buildings_client_id', 'buildings', ['client_id'])

    # Create apartments table
    op.create_table(
        'apartments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('number', sa.String(50), nullable=False),
        sa.Column('floor', sa.String(20), nullable=True),
        sa.Column('tenant_name', sa.String(255), nullable=True),
        sa.Column('tenant_phone', sa.String(50), nullable=True),
        sa.Column('tenant_email', sa.String(255), nullable=True),
        sa.Column('building_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('buildings.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )
    op.create_index('ix_apartments_building_id', 'apartments', ['building_id'])
    op.create_index('ix_apartments_number_building', 'apartments', ['building_id', 'number'], unique=True)

    # Create locations table
    op.create_table(
        'locations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('type', postgresql.ENUM('cocina', 'lavadero', 'sala', 'recamara', 'bano', 'pasillo', 'estacionamiento', 'bodega', 'oficina', 'otro', name='locationtype'), nullable=False),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('apartment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('apartments.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )
    op.create_index('ix_locations_apartment_id', 'locations', ['apartment_id'])

    # Create sensors table
    op.create_table(
        'sensors',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('device_id', sa.String(100), nullable=False, unique=True, index=True),
        sa.Column('model', sa.String(100), nullable=True),
        sa.Column('firmware_version', sa.String(50), nullable=True),
        sa.Column('status', postgresql.ENUM('active', 'inactive', 'alert', 'maintenance', 'disconnected', name='sensorstatus'), nullable=False, server_default='active', index=True),
        sa.Column('gas_threshold_ppm', sa.Integer(), nullable=False, server_default='800'),
        sa.Column('battery_level', sa.Integer(), nullable=True),
        sa.Column('signal_strength', sa.Integer(), nullable=True),
        sa.Column('last_seen', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('location_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('locations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )
    op.create_index('ix_sensors_location_id', 'sensors', ['location_id'])

    # Create sensor_events table (will be converted to hypertable)
    op.create_table(
        'sensor_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('sensor_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('sensors.id', ondelete='CASCADE'), nullable=False),
        sa.Column('event_type', postgresql.ENUM('normal', 'alert', 'warning', 'offline', 'online', name='eventtype'), nullable=False, index=True),
        sa.Column('gas_level', sa.Integer(), nullable=True),
        sa.Column('threshold', sa.Integer(), nullable=True),
        sa.Column('battery_level', sa.Integer(), nullable=True),
        sa.Column('signal_strength', sa.Integer(), nullable=True),
        sa.Column('raw_data', postgresql.JSONB(), nullable=True),
        sa.Column('timestamp', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('timestamp', 'id')
    )
    op.create_index('ix_sensor_events_sensor_id', 'sensor_events', ['sensor_id'])

    # Create contacts table
    op.create_table(
        'contacts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('phone', sa.String(50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('client_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )
    op.create_index('ix_contacts_client_id', 'contacts', ['client_id'])

    # Create notifications table
    op.create_table(
        'notifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('sensor_event_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('contact_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('contacts.id', ondelete='SET NULL'), nullable=True),
        sa.Column('channel', postgresql.ENUM('email', 'sms', name='notificationchannel'), nullable=False),
        sa.Column('recipient', sa.String(255), nullable=False),
        sa.Column('subject', sa.String(255), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('status', postgresql.ENUM('pending', 'sent', 'failed', name='notificationstatus'), nullable=False, server_default='pending', index=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('sent_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )
    op.create_index('ix_notifications_contact_id', 'notifications', ['contact_id'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('notifications')
    op.drop_table('contacts')
    op.drop_table('sensor_events')
    op.drop_table('sensors')
    op.drop_table('locations')
    op.drop_table('apartments')
    op.drop_table('buildings')
    op.drop_table('clients')
    op.drop_table('users')

    # Drop ENUM types
    op.execute('DROP TYPE IF EXISTS notificationstatus')
    op.execute('DROP TYPE IF EXISTS notificationchannel')
    op.execute('DROP TYPE IF EXISTS locationtype')
    op.execute('DROP TYPE IF EXISTS eventtype')
    op.execute('DROP TYPE IF EXISTS sensorstatus')
    op.execute('DROP TYPE IF EXISTS userrole')
