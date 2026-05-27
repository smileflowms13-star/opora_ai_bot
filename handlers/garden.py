from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from database import get_streak
from texts import GARDEN_TITLE, GARDEN_SEEDLING, GARDEN_FLOWER, GARDEN_TREE, GARDEN_BUTTON

router = Router()

def build_garden(telegram_id: int) -> str:
    streak = get_streak(telegram_id)
    text = GARDEN_TITLE
    if streak["current_streak"] >= 30:
        text += GARDEN_TREE
    elif streak["current_streak"] >= 7:
        text += GARDEN_FLOWER
    else:
        text += GARDEN_SEEDLING
    text += f"\n\nТекущий стрик: {streak['current_streak']} дн. • Лучший: {streak['longest_streak']} дн."
    return text

@router.message(Command("garden"))
@router.message(F.text == GARDEN_BUTTON)
async def garden_command(message: Message):
    if not message.from_user:
        await message.answer("Не смог определить пользователя.")
        return
    await message.answer(build_garden(message.from_user.id))