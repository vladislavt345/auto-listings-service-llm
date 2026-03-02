"""Repository for user persistence operations."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


class UserRepository:
    """Provide CRUD operations for users."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize repository with active session.

        Args:
            db: Active SQLAlchemy session.
        """

        self.db = db

    async def get_by_username(self, username: str) -> User | None:
        """Find a user by username.

        Args:
            username: Unique username.

        Returns:
            User if found, otherwise None.
        """

        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def create(self, username: str, hashed_password: str) -> User:
        """Create and persist a user record.

        Args:
            username: Unique username.
            hashed_password: Password hash.

        Returns:
            Persisted user entity.
        """

        user = User(username=username, hashed_password=hashed_password)
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
