import asyncio
import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database import get_connection
from aiogram import Bot

logger = logging.getLogger(__name__)

REMINDER_MESSAGE = (
    "Привет! \U0001F319 Самое время для вечерней записи в дневник.\n"
    "Как прошёл твой день? Оцени настроение от 1 до 10, а если хочешь — напиши, что было важного."
)

async def send_daily_reminders(bot: Bot):
    """Проверяет всех пользователей и отправляет напоминания, если пора."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        now_utc = datetime.utcnow().strftime("%H:%M")
        cursor.execute(
            """
            SELECT telegram_id FROM users
            WHERE daily_reminder_enabled = 1 AND daily_reminder_time = ?
            """,
            (now_utc,),
        )
        rows = cursor.fetchall()
        for row in rows:
            telegram_id = row[0]
            try:
                await bot.send_message(telegram_id, REMINDER_MESSAGE)
                logger.info(f"Sent daily reminder to {telegram_id}")
            except Exception as e:
                logger.warning(f"Could not send reminder to {telegram_id}: {e}")
    except Exception as e:
        logger.exception("Error in daily reminder job")
    finally:
        conn.close()

def setup_scheduler(bot: Bot):
    loop = asyncio.get_running_loop()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        lambda: asyncio.run_coroutine_threadsafe(send_daily_reminders(bot), loop),
        'cron',
        minute='*',
        id='daily_reminder',
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started")
    return scheduler


