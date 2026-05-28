from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.analytics import get_personalized_suggestion
from keyboards import main_menu

router = Router()

@router.message(Command("suggest"))
async def suggest_command(message: Message):
    if not message.from_user:
        await message.answer("Не смог определить пользователя.")
        return

    suggestion = get_personalized_suggestion(message.from_user.id)
    await message.answer(f"💡 Персональная рекомендация:\n\n{suggestion}", reply_markup=main_menu)