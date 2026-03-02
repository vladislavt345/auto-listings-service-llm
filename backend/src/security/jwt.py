"""JWT token helpers."""

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from jwt import InvalidTokenError

from src.config.settings import get_settings

settings = get_settings()


def create_access_token(subject: str) -> str:
    """Create signed JWT for subject."""

    expire = datetime.now(UTC) + timedelta(minutes=settings.jwt_exp_minutes)
    payload: dict[str, Any] = {"sub": subject, "exp": int(expire.timestamp())}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict[str, Any] | None:
    """Decode and validate JWT token."""

    try:
        return jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
    except InvalidTokenError:
        return None
