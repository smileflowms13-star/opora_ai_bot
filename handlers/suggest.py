from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from services.analytics import get_personalized_suggestion
from keyboards import get_main_menu
from services.i18n import get_text

router = Router()

@router.message(Command("suggest"))
async def suggest_command(message: Message, **kwargs):
    if not message.from_user:
        await message.answer("Не смог определить пользователя.")
        return
    lang = kwargs.get("lang", "ru")
    suggestion = get_personalized_suggestion(message.from_user.id)
    prefix = get_text("suggest_prefix", lang)
    await message.answer(f"{prefix}\n\n{suggestion}", reply_markup=get_main_menu(lang))