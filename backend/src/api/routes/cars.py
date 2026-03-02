"""Car listing API routes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies.auth import get_current_user
from src.constants import API_PREFIX, ROUTE_CARS, TAG_CARS
from src.db.session import get_db
from src.models.user import User
from src.schemas.car import CarFilter, CarResponse
from src.services.car_service import CarService

router = APIRouter(prefix=API_PREFIX, tags=[TAG_CARS])


@router.get(ROUTE_CARS, response_model=list[CarResponse])
async def list_cars(
    make: str | None = Query(default=None),
    model: str | None = Query(default=None),
    color: str | None = Query(default=None),
    max_price: float | None = Query(default=None),
    min_year: int | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    _user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[CarResponse]:
    """Return protected car listing collection.

    Args:
        make: Optional make filter.
        model: Optional model filter.
        color: Optional color filter.
        max_price: Optional maximum price filter.
        min_year: Optional minimum year filter.
        limit: Maximum number of records to return.
        offset: Number of records to skip.
        _user: Authenticated user dependency.
        db: Active SQLAlchemy session.

    Returns:
        Filtered list of serialized car listings.
    """

    filters = CarFilter(
        make=make, model=model, color=color, max_price=max_price, min_year=min_year
    )
    return await CarService(db).list_cars(filters, limit=limit, offset=offset)
