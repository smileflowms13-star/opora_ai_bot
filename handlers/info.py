from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards import get_main_menu
from services.i18n import get_text

router = Router()

@router.message(Command("help"))
async def help_command(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("help_text", lang), reply_markup=get_main_menu(lang))

@router.message(Command("rules"))
async def rules_command(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("rules_text", lang), reply_markup=get_main_menu(lang))

@router.message(Command("privacy"))
async def privacy_command(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("privacy_text", lang), reply_markup=get_main_menu(lang))