"""
Database Connection and Session Management
Uses SQLAlchemy 2.0 with async support
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
import logging

from app.config import settings

logger = logging.getLogger(__name__)

# Create async engine
# Replace postgresql:// with postgresql+asyncpg://
database_url = settings.database_url.replace(
    "postgresql://",
    "postgresql+asyncpg://"
)

engine = create_async_engine(
    database_url,
    echo=settings.debug,  # Log SQL queries in debug mode
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_pre_ping=True,  # Verify connections before using
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for all models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for FastAPI endpoints to get database session.

    Usage:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Initialize database - create all tables.
    This is mainly for development/testing.
    In production, use Alembic migrations.
    """
    async with engine.begin() as conn:
        # Import all models to ensure they're registered
        from app.models import (
            user, client, building, apartment,
            location, sensor, sensor_event, contact, notification
        )

        logger.info("Creating database tables...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Database tables created")


async def drop_db():
    """
    Drop all tables - USE WITH CAUTION!
    Only for development/testing.
    """
    async with engine.begin() as conn:
        logger.warning("⚠️ Dropping all database tables...")
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("✅ Database tables dropped")


async def check_db_connection():
    """Check if database connection is working."""
    try:
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        logger.info("✅ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False
