"""Repository protocol definitions for dependency inversion in services."""

from collections.abc import Iterable
from typing import Protocol

from src.models.car import Car
from src.models.user import User
from src.schemas.car import CarFilter, CarUpsertPayload


class CarRepositoryProtocol(Protocol):
    """Contract for car repository operations used by services."""

    async def get_many(
        self, filters: CarFilter | None = None, limit: int = 50, offset: int = 0
    ) -> list[Car]: ...

    async def upsert_many(
        self, items: Iterable[CarUpsertPayload]
    ) -> tuple[int, int]: ...


class UserRepositoryProtocol(Protocol):
    """Contract for user repository operations used by services."""

    async def get_by_username(self, username: str) -> User | None: ...

    async def create(self, username: str, hashed_password: str) -> User: ...
