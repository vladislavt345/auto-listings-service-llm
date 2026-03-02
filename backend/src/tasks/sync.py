"""ARQ jobs for listing synchronization."""

import asyncio
import logging
from typing import Any

from src.adapters.base import BaseListingsAdapter
from src.adapters.carsensor import CarSensorAdapter
from src.config.settings import get_settings
from src.db.session import session_scope
from src.services.car_service import CarService

logger = logging.getLogger(__name__)
settings = get_settings()


async def sync_cars(ctx: dict[str, Any]) -> dict[str, int]:
    """Fetch and upsert car listings with retry/backoff."""

    last_error: Exception | None = None
    attempts = max(settings.scraper_retry_attempts, 1)
    adapter: BaseListingsAdapter = ctx.get("adapter", CarSensorAdapter())

    for attempt in range(1, attempts + 1):
        try:
            rows = await adapter.fetch()
            async with session_scope() as db:
                inserted, updated = await CarService(db).upsert_cars(rows)
            payload = {"fetched": len(rows), "inserted": inserted, "updated": updated}
            logger.info("ARQ sync done: %s", payload)
            return payload
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt >= attempts:
                break
            delay = min(2 ** (attempt - 1), 15)
            logger.warning(
                "ARQ sync failed (attempt %s/%s): %s. Retry in %ss",
                attempt,
                attempts,
                exc,
                delay,
            )
            await asyncio.sleep(delay)

    raise RuntimeError(
        f"ARQ sync failed after {attempts} attempts: {last_error}"
    ) from last_error
