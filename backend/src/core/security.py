"""Backward-compatible imports for split JWT/password modules."""

from src.core.jwt import create_access_token, decode_token
from src.core.password import hash_password, verify_password
