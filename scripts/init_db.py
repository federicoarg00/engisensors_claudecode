"""
Database Initialization Script

Creates all tables and sets up TimescaleDB hypertable for sensor_events.

Usage:
    python scripts/init_db.py
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'backend'))

from sqlalchemy import text
from app.database import engine, Base
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_timescaledb_extension():
    """Enable TimescaleDB extension in PostgreSQL."""
    async with engine.begin() as conn:
        try:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE"))
            logger.info("✅ TimescaleDB extension enabled")
        except Exception as e:
            logger.error(f"❌ Failed to create TimescaleDB extension: {e}")
            logger.error("Make sure you're using TimescaleDB image: timescale/timescaledb")
            raise


async def create_hypertable():
    """Convert sensor_events table to TimescaleDB hypertable."""
    async with engine.begin() as conn:
        try:
            # Check if hypertable already exists
            result = await conn.execute(text("""
                SELECT * FROM timescaledb_information.hypertables
                WHERE hypertable_name = 'sensor_events'
            """))

            if result.fetchone():
                logger.info("⏭️ Hypertable 'sensor_events' already exists")
                return

            # Create hypertable with timestamp as the time dimension
            await conn.execute(text("""
                SELECT create_hypertable(
                    'sensor_events',
                    'timestamp',
                    if_not_exists => TRUE,
                    migrate_data => TRUE
                )
            """))
            logger.info("✅ Created hypertable 'sensor_events' with time dimension 'timestamp'")

            # Set compression policy (compress data older than 7 days)
            await conn.execute(text("""
                ALTER TABLE sensor_events SET (
                    timescaledb.compress,
                    timescaledb.compress_segmentby = 'sensor_id'
                )
            """))
            logger.info("✅ Enabled compression on 'sensor_events'")

            # Create compression policy
            await conn.execute(text("""
                SELECT add_compression_policy('sensor_events', INTERVAL '7 days')
            """))
            logger.info("✅ Added compression policy (compress after 7 days)")

            # Create retention policy (delete data older than 2 years)
            await conn.execute(text("""
                SELECT add_retention_policy('sensor_events', INTERVAL '2 years')
            """))
            logger.info("✅ Added retention policy (delete after 2 years)")

        except Exception as e:
            logger.error(f"❌ Failed to create hypertable: {e}")
            raise


async def create_indexes():
    """Create additional indexes for performance."""
    async with engine.begin() as conn:
        try:
            # Composite index for sensor_id + timestamp (common query pattern)
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_sensor_events_sensor_timestamp
                ON sensor_events (sensor_id, timestamp DESC)
            """))

            # Index for event_type + timestamp (filtering alerts)
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_sensor_events_type_timestamp
                ON sensor_events (event_type, timestamp DESC)
            """))

            logger.info("✅ Created performance indexes")
        except Exception as e:
            logger.warning(f"⚠️ Failed to create some indexes: {e}")


async def init_database():
    """Initialize the database with all tables and configurations."""
    logger.info("🚀 Starting database initialization...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Database: {settings.database_url}")

    try:
        # Step 1: Enable TimescaleDB extension
        logger.info("\n📦 Step 1: Enabling TimescaleDB extension...")
        await create_timescaledb_extension()

        # Step 2: Create all tables
        logger.info("\n📊 Step 2: Creating database tables...")
        async with engine.begin() as conn:
            # Import all models to ensure they're registered
            from app.models import (
                user, client, building, apartment,
                location, sensor, sensor_event, contact, notification
            )

            await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ All tables created")

        # Step 3: Convert sensor_events to hypertable
        logger.info("\n⏰ Step 3: Setting up TimescaleDB hypertable...")
        await create_hypertable()

        # Step 4: Create additional indexes
        logger.info("\n🔍 Step 4: Creating performance indexes...")
        await create_indexes()

        logger.info("\n✅ Database initialization completed successfully!")
        logger.info("\n📝 Next steps:")
        logger.info("   1. Run: python scripts/create_admin.py  (create admin user)")
        logger.info("   2. Start backend: docker-compose up backend")
        logger.info("   3. Test: curl http://localhost:8000/health")

    except Exception as e:
        logger.error(f"\n❌ Database initialization failed: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_database())
