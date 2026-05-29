from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards import get_main_menu
from services.map_builder import build_user_map
from services.i18n import get_text

router = Router()

@router.message(Command("map"))
@router.message(F.text.in_([get_text("map_button_text", "ru"), get_text("map_button_text", "en")]))
async def map_command(message: Message, **kwargs):
    if not message.from_user:
        await message.answer("Не смог определить пользователя.", reply_markup=get_main_menu(lang))
        return
    lang = kwargs.get("lang", "ru")
    user_map = build_user_map(message.from_user.id)
    await message.answer(user_map, reply_markup=get_main_menu(lang))