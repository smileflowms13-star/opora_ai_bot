from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import main_menu
from map_builder import build_user_map


router = Router()


@router.message(Command("map"))
@router.message(F.text == "📊 Моя карта")
async def map_command(message: Message):
    if not message.from_user:
        await message.answer("Не смог определить пользователя.", reply_markup=main_menu)
        return

    user_map = build_user_map(message.from_user.id)

    await message.answer(user_map, reply_markup=main_menu)