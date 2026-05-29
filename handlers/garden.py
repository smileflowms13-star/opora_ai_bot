from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards import get_main_menu
from database import get_streak
from services.i18n import get_text

router = Router()

@router.message(Command("garden"))
@router.message(F.text.in_([get_text("garden_button", "ru"), get_text("garden_button", "en")]))
async def garden_command(message: Message, **kwargs):
    if not message.from_user:
        await message.answer("Не смог определить пользователя.", reply_markup=get_main_menu(lang))
        return
    lang = kwargs.get("lang", "ru")
    streak_data = get_streak(message.from_user.id)
    title = get_text("garden_title", lang)
    if streak_data["current_streak"] >= 30:
        plant = get_text("garden_tree", lang)
    elif streak_data["current_streak"] >= 7:
        plant = get_text("garden_flower", lang)
    else:
        plant = get_text("garden_seedling", lang)
    await message.answer(title + plant, reply_markup=get_main_menu(lang))