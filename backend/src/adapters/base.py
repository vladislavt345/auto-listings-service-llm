"""Abstract base class for external car listing adapters."""

from abc import ABC, abstractmethod

from src.schemas.car import CarUpsertPayload


class BaseListingsAdapter(ABC):
    """Protocol for fetching and normalizing car listings from an external source."""

    @abstractmethod
    async def fetch(self) -> list[CarUpsertPayload]:
        """Fetch and return normalized car listings.

        Returns:
            List of normalized listings ready for upsert.

        Raises:
            RuntimeError: If the external source is unavailable.
        """
