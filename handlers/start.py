from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

from database import set_user_consent, user_has_consent, save_onboarding, get_user_language, set_user_language
from keyboards import get_main_menu, get_onboarding_menu, get_focus_menu
from services.i18n import get_text

class OnboardingStates(StatesGroup):
    focus = State()

class LanguageSelection(StatesGroup):
    waiting = State()

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, **kwargs):
    user = message.from_user
    if user and user_has_consent(user.id):
        # Уже зарегистрирован – показываем главное меню на его языке
        lang = kwargs.get("lang", "ru")
        await message.answer(
            get_text("consent_accepted_text", lang),
            reply_markup=get_main_menu(lang),
        )
        return

    # Пользователь ещё не давал согласия
    # Проверяем, выбрал ли он уже язык (мог начать онбординг раньше)
    lang = get_user_language(user.id) if user else None
    if lang:
        # Язык уже сохранён – сразу к согласию
        await state.set_state(OnboardingStates.focus)
        await message.answer(
            get_text("onboarding_text", lang),
            reply_markup=get_onboarding_menu(lang),
        )
    else:
        # Первый запуск – предлагаем выбрать язык
        await state.set_state(LanguageSelection.waiting)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="start_lang_ru")],
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="start_lang_en")],
        ])
        # Приглашение выводим на двух языках, так как язык ещё не известен
        await message.answer(
            "Выбери язык / Choose language:",
            reply_markup=keyboard,
        )

@router.callback_query(StateFilter(LanguageSelection.waiting), F.data.startswith("start_lang_"))
async def set_start_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[2]  # start_lang_ru → ru
    user = callback.from_user
    if user:
        set_user_language(user.id, lang)
    await state.clear()
    # Сообщаем о выборе и сразу показываем онбординг на выбранном языке
    await callback.message.edit_text(get_text("language_changed", lang))
    await callback.message.answer(
        get_text("onboarding_text", lang),
        reply_markup=get_onboarding_menu(lang),
    )
    await callback.answer()

# Остальные обработчики остаются без изменений, но теперь они используют **kwargs для получения языка
@router.message(F.text.in_([get_text("consent_accept_button", "ru"), get_text("consent_accept_button", "en")]))
async def accept_consent(message: Message, state: FSMContext, **kwargs):
    user = message.from_user
    if user is None:
        return
    set_user_consent(user.id, True)
    await state.set_state(OnboardingStates.focus)
    lang = kwargs.get("lang", "ru")
    await message.answer(
        get_text("focus_question_text", lang),
        reply_markup=get_focus_menu(lang),
    )

@router.message(F.text.in_([get_text("consent_decline_button", "ru"), get_text("consent_decline_button", "en")]))
async def decline_consent(message: Message, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(
        get_text("under_18_text", lang),
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(StateFilter(OnboardingStates.focus))
async def onboarding_focus(message: Message, state: FSMContext, **kwargs):
    user = message.from_user
    if user is None:
        return
    lang = kwargs.get("lang", "ru")
    focus_buttons = [
        get_text("focus_anxiety_button", "ru"),
        get_text("focus_relationships_button", "ru"),
        get_text("focus_relax_button", "ru"),
        get_text("focus_diary_button", "ru"),
        get_text("focus_other_button", "ru"),
        get_text("focus_anxiety_button", "en"),
        get_text("focus_relationships_button", "en"),
        get_text("focus_relax_button", "en"),
        get_text("focus_diary_button", "en"),
        get_text("focus_other_button", "en"),
    ]
    if message.text in focus_buttons:
        save_onboarding(user.id, message.text)
        await state.clear()
        await message.answer(
            get_text("focus_changed_text", lang),
            reply_markup=get_main_menu(lang),
        )
        await message.delete()
    else:
        await message.answer(
            get_text("focus_question_text", lang),
            reply_markup=get_focus_menu(lang),
        )