"""Authentication business logic."""

from sqlalchemy.ext.asyncio import AsyncSession

from src.security.jwt import create_access_token
from src.security.password import verify_password
from src.repositories.protocols import UserRepositoryProtocol
from src.repositories.user_repository import UserRepository
from src.schemas.auth import TokenResponse


class AuthService:
    """Authenticate users and issue JWT tokens."""

    def __init__(
        self, db: AsyncSession, repo: UserRepositoryProtocol | None = None
    ) -> None:
        """Initialize service with active session.

        Args:
            db: Active SQLAlchemy session.
        """

        self.repo: UserRepositoryProtocol = repo or UserRepository(db)

    async def login(self, username: str, password: str) -> TokenResponse | None:
        """Validate credentials and issue token.

        Args:
            username: Login username.
            password: Plain-text password.

        Returns:
            Token response on success, otherwise None.
        """

        user = await self.repo.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return TokenResponse(access_token=create_access_token(user.username))
