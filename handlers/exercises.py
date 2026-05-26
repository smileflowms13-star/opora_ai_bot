import logging
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from texts import (
    BREATHING_INTRO, BREATHING_STEP_INHALE, BREATHING_STEP_HOLD_IN,
    BREATHING_STEP_EXHALE, BREATHING_STEP_HOLD_OUT, BREATHING_FINISH,
    BREATHING_BUTTON
)
from keyboards import breathing_continue_keyboard, breathing_finish_keyboard, main_menu

router = Router()

class BreathingSteps(StatesGroup):
    intro = State()
    inhale = State()
    hold_in = State()
    exhale = State()
    hold_out = State()
    finish = State()

@router.message(F.text == BREATHING_BUTTON)
async def start_breathing(message: Message, state: FSMContext):
    logging.info(f"User {message.from_user.id} started breathing exercise")
    await state.set_state(BreathingSteps.intro)
    msg = await message.answer(BREATHING_INTRO, reply_markup=breathing_continue_keyboard())
    await state.update_data(exercise_msg_id=msg.message_id)

@router.callback_query(F.data == "breathing_next")
async def next_step(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == BreathingSteps.intro.state:
        await state.set_state(BreathingSteps.inhale)
        await callback.message.edit_text(BREATHING_STEP_INHALE, reply_markup=breathing_continue_keyboard())
    elif current_state == BreathingSteps.inhale.state:
        await state.set_state(BreathingSteps.hold_in)
        await callback.message.edit_text(BREATHING_STEP_HOLD_IN, reply_markup=breathing_continue_keyboard())
    elif current_state == BreathingSteps.hold_in.state:
        await state.set_state(BreathingSteps.exhale)
        await callback.message.edit_text(BREATHING_STEP_EXHALE, reply_markup=breathing_continue_keyboard())
    elif current_state == BreathingSteps.exhale.state:
        await state.set_state(BreathingSteps.hold_out)
        await callback.message.edit_text(BREATHING_STEP_HOLD_OUT, reply_markup=breathing_continue_keyboard())
    elif current_state == BreathingSteps.hold_out.state:
        await state.set_state(BreathingSteps.finish)
        await callback.message.edit_text(BREATHING_FINISH, reply_markup=breathing_finish_keyboard())
    elif current_state == BreathingSteps.finish.state:
        await exit_breathing(callback, state)
        return
    await callback.answer()

@router.callback_query(F.data == "breathing_exit")
async def exit_breathing(callback: CallbackQuery, state: FSMContext):
    logging.info(f"User {callback.from_user.id} exited breathing exercise")
    await state.clear()
    await callback.message.edit_text("Главное меню", reply_markup=None)
    await callback.message.answer("Вы вернулись в главное меню.", reply_markup=main_menu)
    await callback.answer()

@router.message(Command("cancel"))
async def cancel_breathing(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Упражнение прервано. Ты в главном меню.", reply_markup=main_menu)

