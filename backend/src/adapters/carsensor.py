"""Adapter for loading and normalizing car listings from the CarSensor API."""

import logging
from typing import Any

import httpx

from src.adapters.base import BaseListingsAdapter
from src.config.settings import get_settings
from src.schemas.car import CarUpsertPayload

logger = logging.getLogger(__name__)
settings = get_settings()


class CarSensorAdapter(BaseListingsAdapter):
    """Fetch and normalize external car listing payloads from carsensor.net."""

    async def fetch(self) -> list[CarUpsertPayload]:
        """Load listings from remote API.

        Returns:
            Normalized list of listings.

        Raises:
            RuntimeError: If HTTP request fails.
        """

        try:
            async with httpx.AsyncClient(
                timeout=settings.scraper_timeout_seconds
            ) as client:
                response = await client.get(settings.carsensor_api_url)
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise RuntimeError(f"Failed to fetch cars from source: {exc}") from exc

        payload: list[dict[str, Any]] | dict[str, Any] = response.json()
        return self._normalize(payload)

    def _normalize(
        self, payload: list[dict[str, Any]] | dict[str, Any]
    ) -> list[CarUpsertPayload]:
        """Normalize raw API payload into internal typed format.

        Args:
            payload: Raw API response payload.

        Returns:
            Normalized and validated upsert payload list.
        """

        rows: list[dict[str, Any]] = (
            payload if isinstance(payload, list) else payload.get("items", [])
        )
        normalized: list[CarUpsertPayload] = []
        for row in rows:
            try:
                normalized.append(
                    {
                        "make": str(row.get("make") or row.get("brand") or "").strip(),
                        "model": str(row.get("model") or "").strip(),
                        "year": int(row.get("year")),
                        "price": float(row.get("price")),
                        "color": str(row.get("color") or "").strip(),
                        "source_url": str(
                            row.get("url")
                            or row.get("link")
                            or row.get("source_url")
                            or ""
                        ).strip(),
                    }
                )
            except (TypeError, ValueError):
                continue

        return [
            row
            for row in normalized
            if row["make"]
            and row["model"]
            and row["year"]
            and row["price"]
            and row["color"]
            and row["source_url"]
        ]
