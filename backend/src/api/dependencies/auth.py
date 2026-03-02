"""Authentication dependencies for protected endpoints."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.constants import ERROR_INVALID_TOKEN, ERROR_USER_NOT_FOUND
from src.core.jwt import decode_token
from src.db.session import get_db
from src.models.user import User
from src.repositories.protocols import UserRepositoryProtocol
from src.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer()


def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepositoryProtocol:
    """Provide user repository dependency."""

    return UserRepository(db)


async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    repo: UserRepositoryProtocol = Depends(get_user_repo),
) -> User:
    """Resolve current user from bearer token.

    Args:
        creds: Parsed HTTP bearer credentials.
        repo: User repository dependency.

    Returns:
        Authenticated user entity.

    Raises:
        HTTPException: If token is invalid or user is not found.
    """

    payload = decode_token(creds.credentials)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=ERROR_INVALID_TOKEN
        )

    user = await repo.get_by_username(str(payload["sub"]))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=ERROR_USER_NOT_FOUND
        )
    return user
