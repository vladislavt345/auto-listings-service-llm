"""LLM-based filter extraction for natural language search requests."""

import json
import re
from typing import Any

from openai import OpenAI
from src.config.settings import get_settings
from src.schemas.car import CarFilter

settings = get_settings()


class FilterParser:
    """Parse free-form user text into typed car filters."""

    def __init__(self) -> None:
        """Initialize optional LLM client from settings."""

        self.client: OpenAI | None = (
            OpenAI(api_key=settings.llm_api_key) if settings.llm_api_key else None
        )

    def parse(self, text: str) -> CarFilter:
        """Extract filters using LLM function-calling with fallback parser.

        Args:
            text: Raw user request text.

        Returns:
            Parsed car filter model.
        """

        if not self.client:
            return self._fallback_parse(text)

        tool_schema: dict[str, Any] = {
            "name": "extract_car_filters",
            "description": "Extract car search filters from user text",
            "parameters": {
                "type": "object",
                "properties": {
                    "make": {"type": "string"},
                    "model": {"type": "string"},
                    "color": {"type": "string"},
                    "max_price": {"type": "number"},
                    "min_year": {"type": "integer"},
                },
            },
        }

        response = self.client.responses.create(
            model=settings.llm_model,
            input=[{"role": "user", "content": text}],
            tools=[{"type": "function", **tool_schema}],
            tool_choice={
                "type": "function",
                "name": "extract_car_filters",
            },
        )

        for item in response.output:
            if item.type == "function_call" and item.name == "extract_car_filters":
                parsed: dict[str, Any] = json.loads(item.arguments)
                return CarFilter(**parsed)

        return self._fallback_parse(text)

    def _fallback_parse(self, text: str) -> CarFilter:
        """Extract basic filters using regex when LLM is unavailable.

        Args:
            text: Raw user request text.

        Returns:
            Best-effort filter model.
        """

        low = text.lower()
        max_price: float | None = None
        price_match = re.search(r"(?:up to|до)\s*(\d+[\d\s]*)", low)
        if price_match:
            max_price = float(price_match.group(1).replace(" ", ""))

        min_year: int | None = None
        year_match = re.search(r"(?:from|от)\s*(20\d{2}|19\d{2})", low)
        if year_match:
            min_year = int(year_match.group(1))

        return CarFilter(max_price=max_price, min_year=min_year)
