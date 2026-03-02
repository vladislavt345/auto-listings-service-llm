"""Database session management utilities."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config.settings import get_settings

settings = get_settings()

engine = create_async_engine(settings.database_url, pool_pre_ping=True)
session_factory = async_sessionmaker(
    bind=engine, class_=AsyncSession, autoflush=False, autocommit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield a scoped database session for request lifecycle.

    Yields:
        Active SQLAlchemy session.
    """

    async with session_factory() as db:
        try:
            yield db
            await db.commit()
        except Exception:
            await db.rollback()
            raise


@asynccontextmanager
async def session_scope() -> AsyncGenerator[AsyncSession, None]:
    """Provide a shared session lifecycle helper for non-request code."""

    async with session_factory() as db:
        try:
            yield db
            await db.commit()
        except Exception:
            await db.rollback()
            raise
