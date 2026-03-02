"""Authentication API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.constants import API_PREFIX, ERROR_INVALID_CREDENTIALS, ROUTE_LOGIN, TAG_AUTH
from src.db.session import get_db
from src.schemas.auth import LoginRequest, TokenResponse
from src.services.auth_service import AuthService

router = APIRouter(prefix=API_PREFIX, tags=[TAG_AUTH])


@router.post(ROUTE_LOGIN, response_model=TokenResponse)
async def login(
    payload: LoginRequest, db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    """Authenticate user and return JWT token.

    Args:
        payload: Login credentials payload.
        db: Active SQLAlchemy session.

    Returns:
        JWT token response.

    Raises:
        HTTPException: If credentials are invalid.
    """

    token = await AuthService(db).login(payload.username, payload.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=ERROR_INVALID_CREDENTIALS
        )
    return token
