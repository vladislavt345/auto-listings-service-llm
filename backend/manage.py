"""Management script for one-off backend tasks."""

import asyncio

from src.db.session import session_scope
from src.seeds.seed import seed_admin


async def main() -> None:
    """Run management tasks required on startup."""

    async with session_scope() as db:
        await seed_admin(db)


if __name__ == "__main__":
    asyncio.run(main())
