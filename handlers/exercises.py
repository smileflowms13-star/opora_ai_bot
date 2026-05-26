import logging
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter

from texts import (
    BREATHING_INTRO, BREATHING_STEP_INHALE, BREATHING_STEP_HOLD_IN,
    BREATHING_STEP_EXHALE, BREATHING_STEP_HOLD_OUT, BREATHING_FINISH,
    BREATHING_BUTTON,
    GROUNDING_BUTTON, GROUNDING_INTRO, GROUNDING_STEP_SEE,
    GROUNDING_STEP_TOUCH, GROUNDING_STEP_HEAR, GROUNDING_STEP_SMELL,
    GROUNDING_STEP_TASTE, GROUNDING_FINISH
)
from keyboards import breathing_continue_keyboard, breathing_finish_keyboard, main_menu
from keyboards import grounding_continue_keyboard, grounding_finish_keyboard

exercises_router = Router()

class BreathingSteps(StatesGroup):
    intro = State()
    inhale = State()
    hold_in = State()
    exhale = State()
    hold_out = State()
    finish = State()

class GroundingSteps(StatesGroup):
    intro = State()
    see = State()
    touch = State()
    hear = State()
    smell = State()
    taste = State()
    finish = State()

# ===== Дыхание по квадрату =====
@exercises_router.message(F.text == BREATHING_BUTTON)
async def start_breathing(message: Message, state: FSMContext):
    await state.clear()
    logging.info(f"User {message.from_user.id} started breathing exercise")
    await state.set_state(BreathingSteps.intro)
    msg = await message.answer(BREATHING_INTRO, reply_markup=breathing_continue_keyboard())
    await state.update_data(exercise_msg_id=msg.message_id)

@exercises_router.callback_query(F.data == "breathing_next")
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

@exercises_router.callback_query(F.data == "breathing_exit")
async def exit_breathing(callback: CallbackQuery, state: FSMContext):
    logging.info(f"User {callback.from_user.id} exited breathing exercise")
    await state.clear()
    await callback.message.edit_text("Главное меню", reply_markup=None)
    await callback.message.answer("Вы вернулись в главное меню.", reply_markup=main_menu)
    await callback.answer()

@exercises_router.message(Command("cancel"))
async def cancel_breathing(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Упражнение прервано. Ты в главном меню.", reply_markup=main_menu)

# ===== Упражнение 5-4-3-2-1 =====
@exercises_router.message(F.text == GROUNDING_BUTTON)
async def start_grounding(message: Message, state: FSMContext):
    await state.clear()
    logging.info(f"User {message.from_user.id} started grounding exercise")
    await state.set_state(GroundingSteps.intro)
    await message.answer(GROUNDING_INTRO, reply_markup=grounding_continue_keyboard(), parse_mode="HTML")

@exercises_router.callback_query(StateFilter(GroundingSteps.intro), F.data == "grounding_next")
async def grounding_step_see(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GroundingSteps.see)
    await callback.message.edit_text(GROUNDING_STEP_SEE, reply_markup=grounding_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps.see), F.data == "grounding_next")
async def grounding_step_touch(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GroundingSteps.touch)
    await callback.message.edit_text(GROUNDING_STEP_TOUCH, reply_markup=grounding_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps.touch), F.data == "grounding_next")
async def grounding_step_hear(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GroundingSteps.hear)
    await callback.message.edit_text(GROUNDING_STEP_HEAR, reply_markup=grounding_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps.hear), F.data == "grounding_next")
async def grounding_step_smell(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GroundingSteps.smell)
    await callback.message.edit_text(GROUNDING_STEP_SMELL, reply_markup=grounding_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps.smell), F.data == "grounding_next")
async def grounding_step_taste(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GroundingSteps.taste)
    await callback.message.edit_text(GROUNDING_STEP_TASTE, reply_markup=grounding_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps.taste), F.data == "grounding_next")
async def grounding_step_finish(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GroundingSteps.finish)
    await callback.message.edit_text(GROUNDING_FINISH, reply_markup=grounding_finish_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps.finish), F.data == "grounding_exit")
async def grounding_finish_exit(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(GROUNDING_FINISH)
    await callback.message.answer("Вы завершили упражнение. Главное меню:", reply_markup=main_menu)
    await callback.answer()

# Универсальный выход для всех промежуточных состояний
@exercises_router.callback_query(StateFilter(GroundingSteps), F.data == "grounding_exit")
async def exit_grounding(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Упражнение прервано. Возвращаемся в главное меню.")
    await callback.message.answer("Главное меню", reply_markup=main_menu)
    await callback.answer()

# Обработчик /cancel для состояний заземления
@exercises_router.message(StateFilter(GroundingSteps), Command("cancel"))
async def cancel_grounding(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Упражнение отменено. Главное меню:", reply_markup=main_menu)