"""ARQ worker configuration."""

from collections.abc import Awaitable, Callable
from typing import Any

from arq import cron
from arq.connections import RedisSettings

from src.config.settings import get_settings
from src.tasks.sync import sync_cars

settings = get_settings()


def _build_cron_jobs() -> list[Any]:
    interval = max(settings.scraper_interval_seconds, 1)
    if interval < 60:
        seconds = set(range(0, 60, interval))
        return [cron(sync_cars, second=seconds)]

    minute_step = max(1, interval // 60)
    minutes = set(range(0, 60, minute_step))
    return [cron(sync_cars, second=0, minute=minutes)]


class WorkerSettings:
    functions: list[Callable[..., Awaitable[Any]]] = [sync_cars]
    cron_jobs: list[Any] = _build_cron_jobs()
    redis_settings: RedisSettings = RedisSettings(
        host=settings.redis_host,
        port=settings.redis_port,
        database=settings.redis_db,
    )
    job_timeout: int = 300
    max_jobs: int = 10
