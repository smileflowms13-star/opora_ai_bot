from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove

from database import delete_user_data, reset_user_consent, set_daily_reminder, get_daily_reminder_settings, disable_reminder, save_crisis_plan, get_crisis_plan
from keyboards import (
    main_menu,
    settings_menu,
    delete_data_confirm_menu,
    withdraw_consent_confirm_menu,
    onboarding_menu,
    focus_menu,
)
from texts import (
    DAILY_REMINDER_BUTTON,
    DAILY_REMINDER_ON_TEXT,
    DAILY_REMINDER_OFF_TEXT,
    DAILY_REMINDER_TIME_PROMPT,
    DAILY_REMINDER_SET_TEXT,
    REMINDER_DISABLE_BUTTON,
    REMINDER_DISABLED_TEXT,
    REMINDER_ALREADY_DISABLED_TEXT,
    CHANGE_FOCUS_BUTTON,
    FOCUS_QUESTION_TEXT,
    CRISIS_PLAN_BUTTON,
    CRISIS_PLAN_PROMPT,
    CRISIS_PLAN_SAVED,
    CRISIS_PLAN_CURRENT,
    CRISIS_PLAN_EMPTY,
    SETTINGS_BUTTON,
    SETTINGS_TEXT,
    SETTINGS_RULES_BUTTON,
    SETTINGS_PRIVACY_BUTTON,
    SETTINGS_WITHDRAW_CONSENT_BUTTON,
    SETTINGS_DELETE_DATA_BUTTON,
    SETTINGS_BACK_BUTTON,
    SETTINGS_CANCEL_BUTTON,
    DELETE_DATA_CONFIRM_BUTTON,
    WITHDRAW_CONSENT_CONFIRM_BUTTON,
    RULES_TEXT,
    PRIVACY_TEXT,
    DELETE_DATA_WARNING_TEXT,
    WITHDRAW_CONSENT_WARNING_TEXT,
    DATA_DELETED_TEXT,
    CONSENT_WITHDRAWN_TEXT,
)
from handlers.start import OnboardingStates


class ReminderStates(StatesGroup):
    waiting_for_time = State()

class CrisisPlanStates(StatesGroup):
    waiting_for_plan = State()

router = Router()


@router.message(Command("menu"))
async def show_main_menu_command(message: Message):
    await message.answer(
        "Выберите, с чего начнём:",
        reply_markup=main_menu,
    )


@router.message(Command("settings"))
@router.message(F.text == SETTINGS_BUTTON)
async def show_settings(message: Message):
    await message.answer(
        SETTINGS_TEXT,
        reply_markup=settings_menu,
    )


@router.message(Command("rules"))
@router.message(F.text == SETTINGS_RULES_BUTTON)
async def show_rules(message: Message):
    await message.answer(
        RULES_TEXT,
        reply_markup=settings_menu,
    )


@router.message(Command("privacy"))
@router.message(F.text == SETTINGS_PRIVACY_BUTTON)
async def show_privacy(message: Message):
    await message.answer(
        PRIVACY_TEXT,
        reply_markup=settings_menu,
    )


@router.message(Command("delete_my_data"))
@router.message(F.text == SETTINGS_DELETE_DATA_BUTTON)
async def ask_delete_data(message: Message):
    await message.answer(
        DELETE_DATA_WARNING_TEXT,
        reply_markup=delete_data_confirm_menu,
    )


@router.message(F.text == DELETE_DATA_CONFIRM_BUTTON)
async def confirm_delete_data(message: Message):
    user = message.from_user

    if user is None:
        await message.answer(
            "Не получилось определить пользователя.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return

    delete_user_data(user.id)

    await message.answer(
        DATA_DELETED_TEXT,
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(F.text == SETTINGS_WITHDRAW_CONSENT_BUTTON)
async def ask_withdraw_consent(message: Message):
    await message.answer(
        WITHDRAW_CONSENT_WARNING_TEXT,
        reply_markup=withdraw_consent_confirm_menu,
    )


@router.message(F.text == WITHDRAW_CONSENT_CONFIRM_BUTTON)
async def confirm_withdraw_consent(message: Message):
    user = message.from_user

    if user is None:
        await message.answer(
            "Не получилось определить пользователя.",
            reply_markup=onboarding_menu,
        )
        return

    reset_user_consent(user.id)

    await message.answer(
        CONSENT_WITHDRAWN_TEXT,
        reply_markup=onboarding_menu,
    )


@router.message(StateFilter(None), F.text == SETTINGS_CANCEL_BUTTON)
async def cancel_settings_action(message: Message):
    await message.answer(
        SETTINGS_TEXT,
        reply_markup=settings_menu,
    )


@router.message(F.text == SETTINGS_BACK_BUTTON)
@router.message(F.text.contains("Главное меню"))
async def back_to_main_menu(message: Message):
    await message.answer(
        "Выберите, с чего начнём:",
        reply_markup=main_menu,
    )


@router.message(F.text == DAILY_REMINDER_BUTTON)
async def daily_reminder_button(message: Message, state: FSMContext):
    user = message.from_user
    if user is None:
        return
    settings = get_daily_reminder_settings(user.id)
    if settings['enabled']:
        msg = DAILY_REMINDER_ON_TEXT.format(settings['time'])
    else:
        msg = DAILY_REMINDER_OFF_TEXT
    await message.answer(msg + "\n\n" + DAILY_REMINDER_TIME_PROMPT)
    await state.set_state(ReminderStates.waiting_for_time)


@router.message(StateFilter(ReminderStates.waiting_for_time), Command("cancel"))
async def cancel_reminder_time(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Установка напоминания отменена.", reply_markup=settings_menu)


@router.message(StateFilter(ReminderStates.waiting_for_time), F.text == SETTINGS_BACK_BUTTON)
@router.message(StateFilter(ReminderStates.waiting_for_time), F.text.contains("Главное меню"))
async def exit_reminder_to_main(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите, с чего начнём:", reply_markup=main_menu)


@router.message(StateFilter(ReminderStates.waiting_for_time))
async def process_reminder_time(message: Message, state: FSMContext):
    user = message.from_user
    if user is None:
        return
    time_text = message.text.strip()
    import re
    if not re.match(r'^\d{2}:\d{2}$', time_text):
        await message.answer("Пожалуйста, введи время в формате ЧЧ:ММ (например, 21:00). Попробуй ещё раз:\n\nИли нажми /cancel для отмены.")
        return
    set_daily_reminder(user.id, enabled=True, reminder_time=time_text)
    await message.answer(DAILY_REMINDER_SET_TEXT.format(time_text))
    await state.clear()


@router.message(F.text == REMINDER_DISABLE_BUTTON)
async def disable_reminder_handler(message: Message):
    user = message.from_user
    if user is None:
        return
    settings = get_daily_reminder_settings(user.id)
    if not settings['enabled']:
        await message.answer(REMINDER_ALREADY_DISABLED_TEXT, reply_markup=settings_menu)
        return
    disable_reminder(user.id)
    await message.answer(REMINDER_DISABLED_TEXT, reply_markup=settings_menu)


@router.message(F.text == CHANGE_FOCUS_BUTTON)
async def change_focus_start(message: Message, state: FSMContext):
    await state.set_state(OnboardingStates.focus)
    await message.answer(FOCUS_QUESTION_TEXT, reply_markup=focus_menu)


@router.message(F.text == CRISIS_PLAN_BUTTON)
async def crisis_plan_start(message: Message, state: FSMContext):
    user = message.from_user
    if not user:
        return
    current_plan = get_crisis_plan(user.id)
    if current_plan:
        await message.answer(CRISIS_PLAN_CURRENT.format(plan=current_plan))
    else:
        await message.answer(CRISIS_PLAN_EMPTY)
    await message.answer(CRISIS_PLAN_PROMPT)
    await state.set_state(CrisisPlanStates.waiting_for_plan)


@router.message(StateFilter(CrisisPlanStates.waiting_for_plan), Command("cancel"))
@router.message(StateFilter(CrisisPlanStates.waiting_for_plan), F.text == "❌ Отмена")
async def cancel_crisis_plan(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Заполнение кризисного плана отменено.", reply_markup=settings_menu)


@router.message(StateFilter(CrisisPlanStates.waiting_for_plan))
async def process_crisis_plan(message: Message, state: FSMContext):
    user = message.from_user
    if not user:
        return
    plan_text = message.text.strip()
    if not plan_text:
        await message.answer("Пожалуйста, напиши хотя бы одну строчку плана.")
        return
    save_crisis_plan(user.id, plan_text)
    await state.clear()
    await message.answer(CRISIS_PLAN_SAVED, reply_markup=settings_menu)