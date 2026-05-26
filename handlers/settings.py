from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove

from database import delete_user_data, reset_user_consent
from keyboards import (
    main_menu,
    settings_menu,
    delete_data_confirm_menu,
    withdraw_consent_confirm_menu,
    onboarding_menu,
)
from texts import (
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

router = Router()



@router.message(Command("menu"))
async def show_main_menu_command(message: Message):
    await message.answer(
        "\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435, \u0441 \u0447\u0435\u0433\u043e \u043d\u0430\u0447\u043d\u0451\u043c:",
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
@router.message(F.text.contains("\u0413\u043b\u0430\u0432\u043d\u043e\u0435 \u043c\u0435\u043d\u044e"))
async def back_to_main_menu(message: Message):
    await message.answer(
        "Выберите, с чего начнём:",
        reply_markup=main_menu,
    )