"""
Create Admin User Script

Creates an initial admin user for system access.

Usage:
    python scripts/create_admin.py
"""
import asyncio
import sys
import os
from getpass import getpass

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'backend'))

from sqlalchemy import select
from passlib.context import CryptContext
from app.database import AsyncSessionLocal
from app.models.user import User, UserRole
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_admin():
    """Create an admin user interactively."""
    logger.info("🔐 Admin User Creation")
    logger.info("=" * 50)

    # Get admin details from user
    email = input("Admin email: ").strip()
    if not email:
        logger.error("Email is required")
        return

    password = getpass("Admin password: ").strip()
    if not password:
        logger.error("Password is required")
        return

    password_confirm = getpass("Confirm password: ").strip()
    if password != password_confirm:
        logger.error("Passwords do not match")
        return

    if len(password) < 8:
        logger.error("Password must be at least 8 characters")
        return

    async with AsyncSessionLocal() as session:
        try:
            # Check if user already exists
            result = await session.execute(
                select(User).where(User.email == email)
            )
            existing_user = result.scalar_one_or_none()

            if existing_user:
                logger.error(f"❌ User with email '{email}' already exists")
                return

            # Create admin user
            password_hash = pwd_context.hash(password)
            admin_user = User(
                email=email,
                password_hash=password_hash,
                role=UserRole.ADMIN,
                is_active=True
            )

            session.add(admin_user)
            await session.commit()

            logger.info(f"\n✅ Admin user created successfully!")
            logger.info(f"   Email: {email}")
            logger.info(f"   Role: ADMIN")
            logger.info(f"\nYou can now login with these credentials.")

        except Exception as e:
            await session.rollback()
            logger.error(f"❌ Failed to create admin user: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(create_admin())
