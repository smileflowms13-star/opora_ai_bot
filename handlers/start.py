from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

from database import set_user_consent, user_has_consent
from keyboards import main_menu, onboarding_menu
from texts import (
    CONSENT_ACCEPT_BUTTON,
    CONSENT_ACCEPTED_TEXT,
    CONSENT_DECLINE_BUTTON,
    ONBOARDING_TEXT,
    UNDER_18_TEXT,
)

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user

    if user and user_has_consent(user.id):
        await message.answer(
            "Рада видеть вас снова. Я рядом. Выберите, с чего начнём:",
            reply_markup=main_menu,
        )
        return

    await message.answer(
        ONBOARDING_TEXT,
        reply_markup=onboarding_menu,
    )


@router.message(F.text == CONSENT_ACCEPT_BUTTON)
async def accept_consent(message: Message):
    user = message.from_user

    if user is None:
        await message.answer(
            ONBOARDING_TEXT,
            reply_markup=onboarding_menu,
        )
        return

    set_user_consent(user.id, True)

    await message.answer(
        CONSENT_ACCEPTED_TEXT,
        reply_markup=main_menu,
    )


@router.message(F.text == CONSENT_DECLINE_BUTTON)
async def decline_consent(message: Message):
    await message.answer(
        UNDER_18_TEXT,
        reply_markup=ReplyKeyboardRemove(),
    )