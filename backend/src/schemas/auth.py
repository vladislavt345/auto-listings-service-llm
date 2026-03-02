"""Authentication request/response schemas."""

from pydantic import BaseModel

from src.constants import TOKEN_TYPE_BEARER


class LoginRequest(BaseModel):
    """Credentials payload for sign in."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """JWT token response payload."""

    access_token: str
    token_type: str = TOKEN_TYPE_BEARER
