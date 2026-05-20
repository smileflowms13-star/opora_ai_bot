import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import init_db
from handlers import diary, fallback, info, map, sections, settings, sos, start, trigger
from logger_config import setup_logging
from middlewares import ConsentMiddleware


logger = logging.getLogger(__name__)


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not configured")

    logger.info("Initializing database")
    init_db()
    logger.info("Database is ready")

    bot = Bot(token=BOT_TOKEN)

    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(ConsentMiddleware())

    dp.include_router(start.router)
    dp.include_router(sos.router)
    dp.include_router(diary.router)
    dp.include_router(trigger.router)
    dp.include_router(map.router)
    dp.include_router(settings.router)
    dp.include_router(sections.router)
    dp.include_router(info.router)

    # Fallback router must be registered last.
    dp.include_router(fallback.router)

    logger.info("Routers registered")
    logger.info("Deleting webhook and dropping pending updates")

    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("Bot polling started. Open Telegram and send /start")

    try:
        await dp.start_polling(bot)
    finally:
        logger.info("Bot polling stopped")


if __name__ == "__main__":
    setup_logging()
    logger.info("Starting Opora AI bot")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Opora AI bot stopped by user")
    except Exception:
        logger.exception("Opora AI bot stopped because of unexpected error")
        raise
    else:
        logger.info("Opora AI bot stopped")
