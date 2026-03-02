"""Car-related API schemas and typed payloads."""

from decimal import Decimal
from typing import TypedDict

from pydantic import BaseModel


class CarResponse(BaseModel):
    """Serialized car listing returned by API."""

    id: int
    make: str
    model: str
    year: int
    price: Decimal
    color: str
    source_url: str

    class Config:
        """Pydantic model configuration."""

        from_attributes = True


class CarFilter(BaseModel):
    """Filter options used by API and bot search."""

    make: str | None = None
    model: str | None = None
    color: str | None = None
    max_price: float | None = None
    min_year: int | None = None


class CarUpsertPayload(TypedDict):
    """Normalized payload used for database upsert operations."""

    make: str
    model: str
    year: int
    price: float
    color: str
    source_url: str
