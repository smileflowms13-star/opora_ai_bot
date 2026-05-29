from aiogram import Router, F
from aiogram.types import Message
from keyboards import get_relationships_menu, get_exercises_menu, get_main_menu
from services.i18n import get_text

router = Router()

@router.message(F.text.in_([get_text("talk_button_text", "ru"), get_text("talk_button_text", "en")]))
async def talk_button(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("talk_text", lang))

@router.message(F.text.in_([get_text("relationships_button_text", "ru"), get_text("relationships_button_text", "en")]))
async def relationships_button(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(
        get_text("relationships_text", lang),
        reply_markup=get_relationships_menu(lang)
    )

@router.message(F.text.in_([get_text("rel_ignored", "ru"), get_text("rel_ignored", "en")]))
async def ignored_button(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("ignored_text", lang))

@router.message(F.text.in_([get_text("rel_jealousy", "ru"), get_text("rel_jealousy", "en")]))
async def jealousy_button(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("jealousy_text", lang))

@router.message(F.text.in_([get_text("rel_cold_partner", "ru"), get_text("rel_cold_partner", "en")]))
async def cold_partner_button(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("cold_partner_text", lang))

@router.message(F.text.in_([get_text("rel_cannot_let_go", "ru"), get_text("rel_cannot_let_go", "en")]))
async def cannot_let_go_button(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("cannot_let_go_text", lang))

@router.message(F.text.in_([get_text("rel_conflicts", "ru"), get_text("rel_conflicts", "en")]))
async def conflicts_button(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("conflicts_text", lang))

@router.message(F.text.in_([get_text("rel_boundary", "ru"), get_text("rel_boundary", "en")]))
async def boundary_button(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("boundary_text", lang))

@router.message(F.text.in_([get_text("rel_help_write", "ru"), get_text("rel_help_write", "en")]))
async def help_write_message_button(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("help_write_text", lang))

@router.message(F.text.in_([get_text("exercises_button_text", "ru"), get_text("exercises_button_text", "en")]))
async def exercises_button(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(
        get_text("choose_exercise_text", lang),
        reply_markup=get_exercises_menu(lang)
    )

@router.message(F.text.in_([get_text("back_to_main_menu_button", "ru"), get_text("back_to_main_menu_button", "en")]))
async def back_to_main_menu(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("back_to_main_menu", lang), reply_markup=get_main_menu(lang))