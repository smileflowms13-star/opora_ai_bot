from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

from database import set_user_consent, user_has_consent, save_onboarding
from keyboards import main_menu, onboarding_menu, focus_menu
from texts import (
    FOCUS_QUESTION_TEXT,
    FOCUS_ANXIETY_BUTTON,
    FOCUS_RELATIONSHIPS_BUTTON,
    FOCUS_RELAX_BUTTON,
    FOCUS_DIARY_BUTTON,
    FOCUS_OTHER_BUTTON,
    CONSENT_ACCEPT_BUTTON,
    CONSENT_ACCEPTED_TEXT,
    CONSENT_DECLINE_BUTTON,
    ONBOARDING_TEXT,
    UNDER_18_TEXT,
)


class OnboardingStates(StatesGroup):
    focus = State()

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
async def accept_consent(message: Message, state: FSMContext):
    user = message.from_user

    if user is None:
        await message.answer(
            ONBOARDING_TEXT,
            reply_markup=onboarding_menu,
        )
        return

    set_user_consent(user.id, True)

    await state.set_state(OnboardingStates.focus)
    await message.answer(
        FOCUS_QUESTION_TEXT,
        reply_markup=focus_menu,
    )


@router.message(StateFilter(OnboardingStates.focus), F.text.in_({FOCUS_ANXIETY_BUTTON, FOCUS_RELATIONSHIPS_BUTTON, FOCUS_RELAX_BUTTON, FOCUS_DIARY_BUTTON, FOCUS_OTHER_BUTTON}))
async def onboarding_focus(message: Message, state: FSMContext):
    user = message.from_user
    if user is None:
        return

    save_onboarding(user.id, message.text)
    await state.clear()
    await message.answer(
        "Спасибо! Теперь я буду учитывать это в наших разговорах.\n\nТы в главном меню.",
        reply_markup=main_menu,
    )
    await message.delete()


# Новый обработчик: если фокус уже выбран, не отправляем кнопку в AI
@router.message(F.text.in_({FOCUS_ANXIETY_BUTTON, FOCUS_RELATIONSHIPS_BUTTON, FOCUS_RELAX_BUTTON, FOCUS_DIARY_BUTTON, FOCUS_OTHER_BUTTON}))
async def focus_already_set(message: Message):
    await message.answer(
        "Твой фокус внимания уже выбран. Если хочешь его изменить, "
        "перейди в Настройки и нажми «🔄 Сменить фокус».",
        reply_markup=main_menu,
    )


@router.message(F.text == CONSENT_DECLINE_BUTTON)
async def decline_consent(message: Message):
    await message.answer(
        UNDER_18_TEXT,
        reply_markup=ReplyKeyboardRemove(),
    )