"""Logging configuration helpers."""

import logging
import sys


def setup_logging() -> None:
    """Configure root logging handlers and formatting."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
