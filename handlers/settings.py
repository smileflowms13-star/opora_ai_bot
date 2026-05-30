import logging, re
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards import (
    get_main_menu, get_settings_menu, get_delete_data_confirm_menu,
    get_withdraw_consent_confirm_menu, get_focus_menu,
)
from database import (
    delete_user_data, reset_user_consent, set_daily_reminder,
    get_daily_reminder_settings, disable_reminder, save_onboarding,
    save_crisis_plan, get_crisis_plan, set_user_language,
)
from services.i18n import get_text

router = Router()
logger = logging.getLogger(__name__)

class ReminderState(StatesGroup):
    waiting_for_time = State()
class CrisisPlanState(StatesGroup):
    waiting_for_plan = State()

# Утилиты для фильтров (рус+англ)
def _btn(key): return [get_text(key, "ru"), get_text(key, "en")]

def _focus_buttons():
    keys = ["focus_anxiety_button", "focus_relationships_button", "focus_relax_button",
            "focus_diary_button", "focus_other_button"]
    btns = []
    for k in keys:
        btns.append(get_text(k, "ru"))
        btns.append(get_text(k, "en"))
    return btns

@router.message(Command("settings"))
@router.message(F.text.in_(_btn("settings_button")))
async def settings_command(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("settings_text", lang), reply_markup=get_settings_menu(lang))

@router.message(F.text.in_(_btn("settings_rules_button")))
async def rules_button(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("rules_text", lang), reply_markup=get_settings_menu(lang))

@router.message(F.text.in_(_btn("settings_privacy_button")))
async def privacy_button(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("privacy_text", lang), reply_markup=get_settings_menu(lang))

@router.message(F.text.in_(_btn("settings_delete_data_button")))
async def delete_data_warning(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("delete_data_warning_text", lang),
                         reply_markup=get_delete_data_confirm_menu(lang))

@router.message(F.text.in_(_btn("delete_data_confirm_button")))
async def delete_data_confirm(message: Message, **kwargs):
    if not message.from_user: return
    delete_user_data(message.from_user.id)
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("data_deleted_text", lang), reply_markup=get_main_menu(lang))

@router.message(F.text.in_(_btn("settings_withdraw_consent_button")))
async def withdraw_consent_warning(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("withdraw_consent_warning_text", lang),
                         reply_markup=get_withdraw_consent_confirm_menu(lang))

@router.message(F.text.in_(_btn("withdraw_consent_confirm_button")))
async def withdraw_consent_confirm(message: Message, **kwargs):
    if not message.from_user: return
    reset_user_consent(message.from_user.id)
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("consent_withdrawn_text", lang), reply_markup=get_main_menu(lang))

@router.message(F.text.in_(_btn("settings_cancel_button")))
async def settings_cancel(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("settings_cancel_text", lang), reply_markup=get_settings_menu(lang))

@router.message(F.text.in_(_btn("settings_back_button")))
async def settings_back(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("back_to_main_menu", lang), reply_markup=get_main_menu(lang))

# Ежедневное напоминание
@router.message(F.text.in_(_btn("daily_reminder_button")))
async def daily_reminder_button(message: Message, state: FSMContext, **kwargs):
    if not message.from_user: return
    settings = get_daily_reminder_settings(message.from_user.id)
    lang = kwargs.get("lang", "ru")
    if settings["enabled"]:
        await message.answer(
            get_text("daily_reminder_on_text", lang).format(settings["time"]),
            reply_markup=get_settings_menu(lang),
        )
        return
    await message.answer(get_text("daily_reminder_time_prompt", lang))
    await state.set_state(ReminderState.waiting_for_time)

@router.message(StateFilter(ReminderState.waiting_for_time))
async def daily_reminder_time(message: Message, state: FSMContext, **kwargs):
    if not message.from_user or not message.text: return
    time_str = message.text.strip()
    lang = kwargs.get("lang", "ru")
    if not re.match(r"^\d{2}:\d{2}$", time_str):
        await message.answer(get_text("daily_reminder_invalid_format", lang))
        return
    set_daily_reminder(message.from_user.id, enabled=True, reminder_time=time_str)
    await state.clear()
    await message.answer(get_text("daily_reminder_set_text", lang).format(time_str),
                         reply_markup=get_settings_menu(lang))

@router.message(F.text.in_(_btn("reminder_disable_button")))
async def disable_reminder_button(message: Message, **kwargs):
    if not message.from_user: return
    settings = get_daily_reminder_settings(message.from_user.id)
    lang = kwargs.get("lang", "ru")
    if not settings["enabled"]:
        await message.answer(get_text("reminder_already_disabled_text", lang),
                             reply_markup=get_settings_menu(lang))
        return
    disable_reminder(message.from_user.id)
    await message.answer(get_text("reminder_disabled_text", lang),
                         reply_markup=get_settings_menu(lang))

# Смена фокуса
@router.message(F.text.in_(_btn("change_focus_button")))
async def change_focus_button(message: Message, state: FSMContext, **kwargs):
    if not message.from_user: return
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("focus_question_text", lang),
                         reply_markup=get_focus_menu(lang))

@router.message(F.text.in_(_focus_buttons()))
async def save_focus(message: Message, **kwargs):
    if not message.from_user: return
    user_id = message.from_user.id
    lang = kwargs.get("lang", "ru")
    save_onboarding(user_id, message.text)
    await message.answer(get_text("focus_changed_text", lang),
                         reply_markup=get_settings_menu(lang))

# Кризисный план
@router.message(F.text.in_(_btn("crisis_plan_button")))
async def crisis_plan_button(message: Message, state: FSMContext, **kwargs):
    if not message.from_user: return
    lang = kwargs.get("lang", "ru")
    plan = get_crisis_plan(message.from_user.id)
    if plan:
        await message.answer(get_text("crisis_plan_current", lang).format(plan=plan),
                             reply_markup=get_settings_menu(lang))
    else:
        await message.answer(get_text("crisis_plan_empty", lang))
        await message.answer(get_text("crisis_plan_prompt", lang))
        await state.set_state(CrisisPlanState.waiting_for_plan)

@router.message(StateFilter(CrisisPlanState.waiting_for_plan))
async def save_crisis_plan_text(message: Message, state: FSMContext, **kwargs):
    if not message.from_user or not message.text: return
    save_crisis_plan(message.from_user.id, message.text.strip())
    lang = kwargs.get("lang", "ru")
    await state.clear()
    await message.answer(get_text("crisis_plan_saved", lang),
                         reply_markup=get_settings_menu(lang))

# Язык
@router.message(F.text.in_(_btn("language_button")))
async def language_settings(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇮🇳 हिन्दी", callback_data="lang_hi")],
        [InlineKeyboardButton(text="🇨🇳 中文", callback_data="lang_zh")],
    ])
    await message.answer(get_text("language_select_text", "ru"), reply_markup=keyboard)

@router.callback_query(F.data.startswith("lang_"))
async def change_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    set_user_language(callback.from_user.id, lang)
    msg = get_text("language_changed", lang)
    await callback.message.edit_text(msg)
    # Автоматически обновляем клавиатуру главного меню на новом языке
    await callback.message.answer(get_text("back_to_main_menu", lang), reply_markup=get_main_menu(lang))
    await callback.answer()