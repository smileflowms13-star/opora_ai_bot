import asyncio
import logging

from middlewares import ConsentMiddleware
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import init_db

from handlers import start, sos, diary, trigger, map, settings, sections, info, fallback


logging.basicConfig(level=logging.INFO)


async def main():
    print("Опора AI запускается...")

    init_db()
    print("База данных готова.")

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

    # fallback всегда последним
    dp.include_router(fallback.router)

    print("Бот запущен. Открой Telegram и напиши /start")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())