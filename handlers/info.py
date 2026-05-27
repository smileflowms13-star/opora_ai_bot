from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from texts import HELP_TEXT, STREAK_INFO_TEXT
from database import get_user_message_count, get_streak


router = Router()


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(HELP_TEXT)


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


@router.message(Command("streak"))
async def streak_command(message: Message):
    if not message.from_user:
        await message.answer("Не смог определить пользователя.")
        return

    streak = get_streak(message.from_user.id)

    await message.answer(
        STREAK_INFO_TEXT.format(
            level_emoji=streak["level_emoji"],
            level_name=streak["level_name"],
            current_streak=streak["current_streak"],
            longest_streak=streak["longest_streak"],
        )
    )