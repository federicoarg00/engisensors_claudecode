"""add user roles and association tables

Revision ID: 20251120_0001
Revises: 20251118_0000_001
Create Date: 2025-11-20 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20251120_0001'
down_revision = '20251118_0000_001'
branch_labels = None
depends_on = None


def upgrade():
    # Update UserRole enum to include new roles
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'building_admin'")
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'owner'")
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'resident'")

    # Create building_admins association table
    op.create_table(
        'building_admins',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('building_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['building_id'], ['buildings.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_building_admins_building_id', 'building_admins', ['building_id'])
    op.create_index('ix_building_admins_user_id', 'building_admins', ['user_id'])

    # Create apartment_owners association table
    op.create_table(
        'apartment_owners',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('apartment_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('is_primary', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['apartment_id'], ['apartments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_apartment_owners_apartment_id', 'apartment_owners', ['apartment_id'])
    op.create_index('ix_apartment_owners_user_id', 'apartment_owners', ['user_id'])

    # Create apartment_residents association table
    op.create_table(
        'apartment_residents',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('apartment_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('added_by_user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['apartment_id'], ['apartments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['added_by_user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_apartment_residents_apartment_id', 'apartment_residents', ['apartment_id'])
    op.create_index('ix_apartment_residents_user_id', 'apartment_residents', ['user_id'])


def downgrade():
    # Drop association tables
    op.drop_index('ix_apartment_residents_user_id', 'apartment_residents')
    op.drop_index('ix_apartment_residents_apartment_id', 'apartment_residents')
    op.drop_table('apartment_residents')

    op.drop_index('ix_apartment_owners_user_id', 'apartment_owners')
    op.drop_index('ix_apartment_owners_apartment_id', 'apartment_owners')
    op.drop_table('apartment_owners')

    op.drop_index('ix_building_admins_user_id', 'building_admins')
    op.drop_index('ix_building_admins_building_id', 'building_admins')
    op.drop_table('building_admins')

    # Note: Cannot remove enum values in PostgreSQL without recreating the enum
    # This would require more complex migration logic with type recreation
