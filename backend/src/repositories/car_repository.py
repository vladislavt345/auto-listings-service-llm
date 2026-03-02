"""Repository for car listing persistence operations."""

from collections.abc import Iterable

from sqlalchemy import literal_column, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.car import Car
from src.schemas.car import CarFilter, CarUpsertPayload


class CarRepository:
    """Provide query and upsert operations for car listings."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize repository with active session.

        Args:
            db: Active SQLAlchemy session.
        """

        self.db = db

    async def get_many(
        self, filters: CarFilter | None = None, limit: int = 50, offset: int = 0
    ) -> list[Car]:
        """Return car listings with optional filtering.

        Args:
            filters: Optional filter set.
            limit: Maximum number of rows to return.
            offset: Number of rows to skip.

        Returns:
            Ordered list of car entities.
        """

        query = select(Car)
        if filters:
            like_filters = {
                "make": Car.make,
                "model": Car.model,
                "color": Car.color,
            }
            for field_name, column in like_filters.items():
                value = getattr(filters, field_name)
                if value:
                    query = query.where(column.ilike(f"%{value}%"))

            if filters.max_price is not None:
                query = query.where(Car.price <= filters.max_price)
            if filters.min_year is not None:
                query = query.where(Car.year >= filters.min_year)
        query = query.order_by(Car.id.desc()).offset(offset).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def upsert_many(self, items: Iterable[CarUpsertPayload]) -> tuple[int, int]:
        """Insert new listings and update changed listings.

        Args:
            items: Normalized iterable of listings.

        Returns:
            Tuple with number of inserted and updated records.
        """

        rows = list(items)
        if not rows:
            return 0, 0

        stmt = insert(Car).values(rows)
        update_fields = {
            "make": stmt.excluded.make,
            "model": stmt.excluded.model,
            "year": stmt.excluded.year,
            "price": stmt.excluded.price,
            "color": stmt.excluded.color,
        }
        stmt = stmt.on_conflict_do_update(
            index_elements=[Car.source_url],
            set_=update_fields,
        )
        stmt = stmt.returning(literal_column("xmax = 0").label("inserted"))
        result = await self.db.execute(stmt)
        inserted_flags = result.scalars().all()

        inserted = sum(1 for flag in inserted_flags if flag)
        updated = len(inserted_flags) - inserted
        return inserted, updated
