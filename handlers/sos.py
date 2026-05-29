from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards import get_sos_menu
from services.i18n import get_text

router = Router()

# Вспомогательная функция для фильтров (рус + англ)
def _btn(key): return [get_text(key, "ru"), get_text(key, "en")]

@router.message(Command("sos"))
async def sos_command(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(
        get_text("sos_intro", lang),
        reply_markup=get_sos_menu(lang),
    )

# Кнопка "Меня накрыло" (из главного меню) – тоже локализована
@router.message(F.text.in_(_btn("sos_button_text")))
async def sos_button(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(
        get_text("sos_intro", lang),
        reply_markup=get_sos_menu(lang),
    )

@router.message(F.text.in_(_btn("sos_anxiety")))
async def anxiety_help(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("anxiety_help_text", lang))

@router.message(F.text.in_(_btn("sos_panic")))
async def panic_help(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("panic_help_text", lang))

@router.message(F.text.in_(_btn("sos_anger")))
async def anger_help(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("anger_help_text", lang))

@router.message(F.text.in_(_btn("sos_cry")))
async def cry_help(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("cry_help_text", lang))

@router.message(F.text.in_(_btn("sos_loneliness")))
async def loneliness_help(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("loneliness_help_text", lang))

@router.message(F.text.in_(_btn("sos_sleep")))
async def sleep_help(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("sleep_help_text", lang))