from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from keyboards import get_main_menu
from database import get_trigger_count
from services.streak_service import process_streak
from services.trigger_service import save_and_format_trigger
from services.i18n import get_text

router = Router()

class TriggerStates(StatesGroup):
    situation = State()
    thought = State()
    emotion = State()
    body_reaction = State()
    impulse = State()
    need = State()

def get_cancel_menu(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=get_text("cancel_button", lang))]],
        resize_keyboard=True
    )

def _btn(key): return [get_text(key, "ru"), get_text(key, "en")]

@router.message(StateFilter(TriggerStates), Command("cancel"))
@router.message(StateFilter(TriggerStates), F.text.in_(_btn("cancel_button")))
async def cancel_trigger(message: Message, state: FSMContext, **kwargs):
    lang = kwargs.get("lang", "ru")
    await state.clear()
    await message.answer(get_text("trigger_cancelled", lang), reply_markup=get_main_menu(lang))

@router.message(Command("trigger"))
@router.message(F.text.in_(_btn("trigger_button_text")))
async def start_trigger(message: Message, state: FSMContext, **kwargs):
    await state.clear()
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("trigger_start_text", lang), reply_markup=get_cancel_menu(lang))
    await state.set_state(TriggerStates.situation)

@router.message(TriggerStates.situation)
async def trigger_situation(message: Message, state: FSMContext, **kwargs):
    situation = (message.text or "").strip()
    lang = kwargs.get("lang", "ru")
    if not situation:
        await message.answer(get_text("trigger_empty_situation", lang))
        return
    await state.update_data(situation=situation)
    await message.answer(get_text("trigger_prompt_thought", lang))
    await state.set_state(TriggerStates.thought)

@router.message(TriggerStates.thought)
async def trigger_thought(message: Message, state: FSMContext, **kwargs):
    thought = (message.text or "").strip()
    lang = kwargs.get("lang", "ru")
    if not thought:
        await message.answer(get_text("trigger_empty_thought", lang))
        return
    await state.update_data(thought=thought)
    await message.answer(get_text("trigger_prompt_emotion", lang))
    await state.set_state(TriggerStates.emotion)

@router.message(TriggerStates.emotion)
async def trigger_emotion(message: Message, state: FSMContext, **kwargs):
    emotion = (message.text or "").strip()
    lang = kwargs.get("lang", "ru")
    if not emotion:
        await message.answer(get_text("trigger_empty_emotion", lang))
        return
    await state.update_data(emotion=emotion)
    await message.answer(get_text("trigger_prompt_body", lang))
    await state.set_state(TriggerStates.body_reaction)

@router.message(TriggerStates.body_reaction)
async def trigger_body(message: Message, state: FSMContext, **kwargs):
    body_reaction = (message.text or "").strip()
    lang = kwargs.get("lang", "ru")
    if not body_reaction:
        await message.answer(get_text("trigger_empty_body", lang))
        return
    await state.update_data(body_reaction=body_reaction)
    await message.answer(get_text("trigger_prompt_impulse", lang))
    await state.set_state(TriggerStates.impulse)

@router.message(TriggerStates.impulse)
async def trigger_impulse(message: Message, state: FSMContext, **kwargs):
    impulse = (message.text or "").strip()
    lang = kwargs.get("lang", "ru")
    if not impulse:
        await message.answer(get_text("trigger_empty_impulse", lang))
        return
    await state.update_data(impulse=impulse)
    await message.answer(get_text("trigger_prompt_need", lang))
    await state.set_state(TriggerStates.need)

@router.message(TriggerStates.need)
async def trigger_need(message: Message, state: FSMContext, **kwargs):
    need = (message.text or "").strip()
    lang = kwargs.get("lang", "ru")
    if not need:
        await message.answer(get_text("trigger_empty_need", lang))
        return
    await state.update_data(need=need)
    data = await state.get_data()
    telegram_id = message.from_user.id if message.from_user else 0

    response = save_and_format_trigger(
        telegram_id=telegram_id,
        situation=data.get("situation"),
        thought=data.get("thought"),
        emotion=data.get("emotion"),
        body_reaction=data.get("body_reaction"),
        impulse=data.get("impulse"),
        need=data.get("need"),
    )

    await state.clear()
    await message.answer(response, reply_markup=get_main_menu(lang))

    streak_msg = process_streak(telegram_id)
    if streak_msg:
        await message.answer(streak_msg)

@router.message(Command("trigger_stats"))
async def trigger_stats_command(message: Message, **kwargs):
    if not message.from_user:
        await message.answer("Не смог определить пользователя.")
        return
    count = get_trigger_count(message.from_user.id)
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("trigger_stats_text", lang).format(count=count), reply_markup=get_main_menu(lang))