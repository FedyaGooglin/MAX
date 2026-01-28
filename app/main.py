import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.bot.router import setup_router
from app.config import load_config
from app.storage.db import init_db


def ensure_data_dir(db_path: Path) -> None:
    data_dir = db_path.parent
    data_dir.mkdir(parents=True, exist_ok=True)


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    setup_router(dp)
    return dp


async def main() -> None:
    config = load_config()
    ensure_data_dir(config.db_path)
    init_db(config.db_path)

    bot = Bot(token=config.token)
    dp = create_dispatcher()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
