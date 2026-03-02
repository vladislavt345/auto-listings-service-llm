"""Backward-compatible imports for split JWT/password modules."""

from src.security.jwt import create_access_token, decode_token
from src.security.password import hash_password, verify_password
