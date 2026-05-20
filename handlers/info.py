from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from texts import HELP_TEXT, RULES_TEXT
from database import get_user_message_count


router = Router()


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(HELP_TEXT)


@router.message(F.text == "📄 Правила и безопасность")
async def rules_button(message: Message):
    await message.answer(RULES_TEXT)


@router.message(F.text == "🔔 Напоминания")
async def reminders_button(message: Message):
    await message.answer(
        "Напоминания появятся позже.\n\n"
        "Мы добавим возможность включить мягкий ежедневный чек-ин:\n"
        "— утром;\n"
        "— вечером;\n"
        "— в удобное время."
    )


@router.message(Command("stats"))
async def stats_command(message: Message):
    if not message.from_user:
        await message.answer("Не смог определить пользователя.")
        return

    count = get_user_message_count(message.from_user.id)

    await message.answer(
        f"Тестовая статистика:\n\n"
        f"Сохранённых сообщений: {count}"
    )