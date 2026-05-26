import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.settings import router as settings_router
from handlers.sos import router as sos_router
from handlers.sections import router as sections_router          # <-- возвращаем
from handlers.exercises import exercises_router
from handlers.diary import router as diary_router
from handlers.trigger import router as trigger_router
from handlers.fallback import router as fallback_router
from scheduler import setup_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

async def main():
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(start_router)
    dp.include_router(settings_router)
    dp.include_router(sos_router)
    dp.include_router(sections_router)       # <-- до exercises
    dp.include_router(exercises_router)
    dp.include_router(diary_router)
    dp.include_router(trigger_router)
    dp.include_router(fallback_router)

    setup_scheduler(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())