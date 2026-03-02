"""Database seed routines."""

from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import get_settings
from src.core.password import hash_password
from src.repositories.user_repository import UserRepository


async def seed_admin(db: AsyncSession) -> None:
    """Create default admin user if it does not exist.

    Args:
        db: Active SQLAlchemy session.
    """

    settings = get_settings()
    users = UserRepository(db)
    if await users.get_by_username(settings.admin_username):
        return
    await users.create(settings.admin_username, hash_password(settings.admin_password))
