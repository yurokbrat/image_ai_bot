import asyncio
import logging
from os import getenv

from aiogram import Bot

from handlers import dp, router


async def main() -> None:
    bot = Bot(token=getenv("TELEGRAM_TOKEN"))  # type: ignore[arg-type]
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
