"""Telegram bot entrypoint for car search interactions."""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from src.config.logger import setup_logging
from src.config.settings import get_settings
from src.db.session import session_scope
from src.services.car_service import CarService

from bot.src.filter_parser import FilterParser

setup_logging()
logger = logging.getLogger(__name__)
settings = get_settings()
dp = Dispatcher()


@dp.message(CommandStart())
async def on_start(message: Message) -> None:
    """Handle `/start` command.

    Args:
        message: Incoming Telegram message object.
    """

    await message.answer("Hi! Send a request like: Find a red BMW up to 2,000,000")


@dp.message()
async def on_search(message: Message) -> None:
    """Handle free-form search requests from Telegram users.

    Args:
        message: Incoming Telegram message object.
    """

    parser = FilterParser()
    filters = parser.parse(message.text or "")

    async with session_scope() as db:
        cars = await CarService(db).list_cars(filters)

    if not cars:
        await message.answer("No listings found.")
        return

    lines = [f"Found listings: {len(cars[:10])}"]
    for car in cars[:10]:
        lines.append(
            f"{car.make} {car.model}, {car.year}, {car.color}, {car.price} | {car.source_url}"
        )

    await message.answer("\n".join(lines))


async def main() -> None:
    """Start Telegram polling loop if bot token is configured."""

    if not settings.telegram_bot_token:
        logger.warning("TELEGRAM_BOT_TOKEN is empty. Bot will not start.")
        return
    bot = Bot(token=settings.telegram_bot_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
