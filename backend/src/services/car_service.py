"""Car listing business logic."""

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.car import Car
from src.repositories.car_repository import CarRepository
from src.repositories.protocols import CarRepositoryProtocol
from src.schemas.car import CarFilter, CarUpsertPayload


class CarService:
    """Coordinate read and write operations for car listings."""

    def __init__(
        self, db: AsyncSession, repo: CarRepositoryProtocol | None = None
    ) -> None:
        """Initialize service with active session.

        Args:
            db: Active SQLAlchemy session.
        """

        self.repo: CarRepositoryProtocol = repo or CarRepository(db)

    async def list_cars(
        self, filters: CarFilter | None = None, limit: int = 50, offset: int = 0
    ) -> list[Car]:
        """Return filtered list of cars.

        Args:
            filters: Optional filter set.
            limit: Maximum number of rows to return.
            offset: Number of rows to skip.

        Returns:
            Matching car entities.
        """

        return await self.repo.get_many(filters, limit=limit, offset=offset)

    async def upsert_cars(self, cars: list[CarUpsertPayload]) -> tuple[int, int]:
        """Upsert normalized car records.

        Args:
            cars: List of normalized listings.

        Returns:
            Tuple with inserted and updated counts.
        """

        rows_by_url: dict[str, CarUpsertPayload] = {}
        for item in cars:
            rows_by_url[item["source_url"]] = item
        deduplicated = list(rows_by_url.values())
        return await self.repo.upsert_many(deduplicated)
