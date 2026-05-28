import logging, re, tempfile, os
from gtts import gTTS
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command, StateFilter
from aiogram.enums import ChatAction

from texts import (
    BREATHING_INTRO, BREATHING_STEP_INHALE, BREATHING_STEP_HOLD_IN,
    BREATHING_STEP_EXHALE, BREATHING_STEP_HOLD_OUT, BREATHING_FINISH,
    BREATHING_BUTTON,
    GROUNDING_BUTTON, GROUNDING_INTRO, GROUNDING_STEP_SEE,
    GROUNDING_STEP_TOUCH, GROUNDING_STEP_HEAR, GROUNDING_STEP_SMELL,
    GROUNDING_STEP_TASTE, GROUNDING_FINISH,
    STOP_BUTTON, STOP_INTRO, STOP_STEP_STOP, STOP_STEP_BREATHE,
    STOP_STEP_OBSERVE, STOP_STEP_PROCEED, STOP_FINISH,
    CONTROL_ZONE_BUTTON, CONTROL_ZONE_INTRO, CONTROL_ZONE_STEP_OUT,
    CONTROL_ZONE_STEP_INFLUENCE, CONTROL_ZONE_STEP_ACTION, CONTROL_ZONE_FINISH,
    SELF_COMPASSION_BUTTON, SELF_COMPASSION_INTRO, SELF_COMPASSION_STEP_TOUCH,
    SELF_COMPASSION_STEP_PHRASE1, SELF_COMPASSION_STEP_PHRASE2,
    SELF_COMPASSION_STEP_PHRASE3, SELF_COMPASSION_STEP_BREATHE, SELF_COMPASSION_FINISH,
    UNSENT_LETTER_BUTTON, UNSENT_LETTER_INTRO, UNSENT_LETTER_STEP_TO,
    UNSENT_LETTER_STEP_EMOTION, UNSENT_LETTER_STEP_SAY, UNSENT_LETTER_STEP_NEED,
    UNSENT_LETTER_FINISH,
    BREATHING_46_BUTTON, BREATHING_46_INTRO, BREATHING_46_STEP_INHALE,
    BREATHING_46_STEP_EXHALE, BREATHING_46_FINISH,
)
from keyboards import (
    breathing_continue_keyboard, breathing_finish_keyboard, main_menu,
    grounding_continue_keyboard, grounding_finish_keyboard,
    stop_continue_keyboard, stop_finish_keyboard,
    control_zone_continue_keyboard, control_zone_finish_keyboard,
    self_compassion_continue_keyboard, self_compassion_finish_keyboard,
    unsent_letter_continue_keyboard, unsent_letter_finish_keyboard,
    breathing46_continue_keyboard, breathing46_finish_keyboard,
)
from services.streak_service import process_streak

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

class StopSteps(StatesGroup):
    intro = State()
    stop = State()
    breathe = State()
    observe = State()
    proceed = State()
    finish = State()

class ControlZoneSteps(StatesGroup):
    intro = State()
    out_of_control = State()
    influence = State()
    action = State()
    finish = State()

class SelfCompassionSteps(StatesGroup):
    intro = State()
    touch = State()
    phrase1 = State()
    phrase2 = State()
    phrase3 = State()
    breathe = State()
    finish = State()

class UnsentLetterSteps(StatesGroup):
    intro = State()
    to = State()
    emotion = State()
    say = State()
    need = State()
    finish = State()

class Breathing46Steps(StatesGroup):
    intro = State()
    inhale = State()
    exhale = State()
    finish = State()

# Общая функция очистки текста от HTML-тегов
def clean_html(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text).strip()

# Общий обработчик озвучки (отправляет аудиофайл вместо голосового сообщения)
@exercises_router.callback_query(F.data == "listen")
async def listen_step(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("current_text")
    if not text:
        # fallback: взять текст из сообщения и очистить
        text = callback.message.text or callback.message.caption or ""
        text = clean_html(text)
    else:
        text = clean_html(text)
    if not text:
        await callback.answer("Нечего озвучивать.")
        return

    await callback.answer("Генерирую аудио...")
    await callback.bot.send_chat_action(chat_id=callback.message.chat.id, action=ChatAction.RECORD_VOICE)

    audio_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tts = gTTS(text=text, lang="ru")
            tts.save(f.name)
            audio_path = f.name
        await callback.message.answer_audio(FSInputFile(audio_path, filename="instruction.mp3"), title="Инструкция")
    except Exception as e:
        logging.exception("TTS failed")
        await callback.message.answer("Не получилось создать аудио. Попробуй позже.")
    finally:
        if audio_path and os.path.exists(audio_path):
            os.unlink(audio_path)

# ===== Дыхание по квадрату =====
@exercises_router.message(F.text == BREATHING_BUTTON)
async def start_breathing(message: Message, state: FSMContext):
    await state.clear()
    logging.info(f"User {message.from_user.id} started breathing exercise")
    await state.set_state(BreathingSteps.intro)
    await state.update_data(current_text=BREATHING_INTRO)
    msg = await message.answer(BREATHING_INTRO, reply_markup=breathing_continue_keyboard())
    await state.update_data(exercise_msg_id=msg.message_id)

@exercises_router.callback_query(F.data == "breathing_next")
async def next_step(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == BreathingSteps.intro.state:
        await state.set_state(BreathingSteps.inhale)
        await state.update_data(current_text=BREATHING_STEP_INHALE)
        await callback.message.edit_text(BREATHING_STEP_INHALE, reply_markup=breathing_continue_keyboard())
    elif current_state == BreathingSteps.inhale.state:
        await state.set_state(BreathingSteps.hold_in)
        await state.update_data(current_text=BREATHING_STEP_HOLD_IN)
        await callback.message.edit_text(BREATHING_STEP_HOLD_IN, reply_markup=breathing_continue_keyboard())
    elif current_state == BreathingSteps.hold_in.state:
        await state.set_state(BreathingSteps.exhale)
        await state.update_data(current_text=BREATHING_STEP_EXHALE)
        await callback.message.edit_text(BREATHING_STEP_EXHALE, reply_markup=breathing_continue_keyboard())
    elif current_state == BreathingSteps.exhale.state:
        await state.set_state(BreathingSteps.hold_out)
        await state.update_data(current_text=BREATHING_STEP_HOLD_OUT)
        await callback.message.edit_text(BREATHING_STEP_HOLD_OUT, reply_markup=breathing_continue_keyboard())
    elif current_state == BreathingSteps.hold_out.state:
        await state.set_state(BreathingSteps.finish)
        await state.update_data(current_text=BREATHING_FINISH)
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
    # Стрик не начисляется при досрочном выходе, поэтому здесь process_streak не вызываем (оставляем как было)
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
    await state.update_data(current_text=GROUNDING_INTRO)
    await message.answer(GROUNDING_INTRO, reply_markup=grounding_continue_keyboard(), parse_mode="HTML")

@exercises_router.callback_query(StateFilter(GroundingSteps.intro), F.data == "grounding_next")
async def grounding_step_see(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GroundingSteps.see)
    await state.update_data(current_text=GROUNDING_STEP_SEE)
    await callback.message.edit_text(GROUNDING_STEP_SEE, reply_markup=grounding_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps.see), F.data == "grounding_next")
async def grounding_step_touch(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GroundingSteps.touch)
    await state.update_data(current_text=GROUNDING_STEP_TOUCH)
    await callback.message.edit_text(GROUNDING_STEP_TOUCH, reply_markup=grounding_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps.touch), F.data == "grounding_next")
async def grounding_step_hear(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GroundingSteps.hear)
    await state.update_data(current_text=GROUNDING_STEP_HEAR)
    await callback.message.edit_text(GROUNDING_STEP_HEAR, reply_markup=grounding_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps.hear), F.data == "grounding_next")
async def grounding_step_smell(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GroundingSteps.smell)
    await state.update_data(current_text=GROUNDING_STEP_SMELL)
    await callback.message.edit_text(GROUNDING_STEP_SMELL, reply_markup=grounding_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps.smell), F.data == "grounding_next")
async def grounding_step_taste(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GroundingSteps.taste)
    await state.update_data(current_text=GROUNDING_STEP_TASTE)
    await callback.message.edit_text(GROUNDING_STEP_TASTE, reply_markup=grounding_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps.taste), F.data == "grounding_next")
async def grounding_step_finish(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GroundingSteps.finish)
    await state.update_data(current_text=GROUNDING_FINISH)
    await callback.message.edit_text(GROUNDING_FINISH, reply_markup=grounding_finish_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps.finish), F.data == "grounding_exit")
async def grounding_finish_exit(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(GROUNDING_FINISH, parse_mode="HTML")
    await callback.message.answer("Вы завершили упражнение. Главное меню:", reply_markup=main_menu)
    # Обновляем стрик через сервис
    streak_msg = process_streak(callback.from_user.id)
    if streak_msg:
        await callback.message.answer(streak_msg)
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps), F.data == "grounding_exit")
async def exit_grounding(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Упражнение прервано. Возвращаемся в главное меню.")
    await callback.message.answer("Главное меню", reply_markup=main_menu)
    await callback.answer()

@exercises_router.message(StateFilter(GroundingSteps), Command("cancel"))
async def cancel_grounding(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Упражнение отменено. Главное меню:", reply_markup=main_menu)

# ===== Упражнение STOP =====
@exercises_router.message(F.text == STOP_BUTTON)
async def start_stop(message: Message, state: FSMContext):
    await state.clear()
    logging.info(f"User {message.from_user.id} started STOP exercise")
    await state.set_state(StopSteps.intro)
    await state.update_data(current_text=STOP_INTRO)
    await message.answer(STOP_INTRO, reply_markup=stop_continue_keyboard(), parse_mode="HTML")

@exercises_router.callback_query(StateFilter(StopSteps.intro), F.data == "stop_next")
async def stop_step_stop(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StopSteps.stop)
    await state.update_data(current_text=STOP_STEP_STOP)
    await callback.message.edit_text(STOP_STEP_STOP, reply_markup=stop_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(StopSteps.stop), F.data == "stop_next")
async def stop_step_breathe(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StopSteps.breathe)
    await state.update_data(current_text=STOP_STEP_BREATHE)
    await callback.message.edit_text(STOP_STEP_BREATHE, reply_markup=stop_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(StopSteps.breathe), F.data == "stop_next")
async def stop_step_observe(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StopSteps.observe)
    await state.update_data(current_text=STOP_STEP_OBSERVE)
    await callback.message.edit_text(STOP_STEP_OBSERVE, reply_markup=stop_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(StopSteps.observe), F.data == "stop_next")
async def stop_step_proceed(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StopSteps.proceed)
    await state.update_data(current_text=STOP_STEP_PROCEED)
    await callback.message.edit_text(STOP_STEP_PROCEED, reply_markup=stop_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(StopSteps.proceed), F.data == "stop_next")
async def stop_step_finish(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StopSteps.finish)
    await state.update_data(current_text=STOP_FINISH)
    await callback.message.edit_text(STOP_FINISH, reply_markup=stop_finish_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(StopSteps.finish), F.data == "stop_exit")
async def stop_finish_exit(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(STOP_FINISH, parse_mode="HTML")
    await callback.message.answer("Вы завершили упражнение. Главное меню:", reply_markup=main_menu)
    streak_msg = process_streak(callback.from_user.id)
    if streak_msg:
        await callback.message.answer(streak_msg)
    await callback.answer()

@exercises_router.callback_query(StateFilter(StopSteps), F.data == "stop_exit")
async def exit_stop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Упражнение прервано. Возвращаемся в главное меню.")
    await callback.message.answer("Главное меню", reply_markup=main_menu)
    await callback.answer()

@exercises_router.message(StateFilter(StopSteps), Command("cancel"))
async def cancel_stop(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Упражнение отменено. Главное меню:", reply_markup=main_menu)

# ===== Упражнение Зона контроля =====
@exercises_router.message(F.text == CONTROL_ZONE_BUTTON)
async def start_control_zone(message: Message, state: FSMContext):
    await state.clear()
    logging.info(f"User {message.from_user.id} started Control Zone exercise")
    await state.set_state(ControlZoneSteps.intro)
    await state.update_data(current_text=CONTROL_ZONE_INTRO)
    await message.answer(CONTROL_ZONE_INTRO, reply_markup=control_zone_continue_keyboard(), parse_mode="HTML")

@exercises_router.callback_query(StateFilter(ControlZoneSteps.intro), F.data == "control_zone_next")
async def control_zone_step_out(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ControlZoneSteps.out_of_control)
    await state.update_data(current_text=CONTROL_ZONE_STEP_OUT)
    await callback.message.edit_text(CONTROL_ZONE_STEP_OUT, reply_markup=control_zone_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(ControlZoneSteps.out_of_control), F.data == "control_zone_next")
async def control_zone_step_influence(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ControlZoneSteps.influence)
    await state.update_data(current_text=CONTROL_ZONE_STEP_INFLUENCE)
    await callback.message.edit_text(CONTROL_ZONE_STEP_INFLUENCE, reply_markup=control_zone_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(ControlZoneSteps.influence), F.data == "control_zone_next")
async def control_zone_step_action(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ControlZoneSteps.action)
    await state.update_data(current_text=CONTROL_ZONE_STEP_ACTION)
    await callback.message.edit_text(CONTROL_ZONE_STEP_ACTION, reply_markup=control_zone_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(ControlZoneSteps.action), F.data == "control_zone_next")
async def control_zone_step_finish(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ControlZoneSteps.finish)
    await state.update_data(current_text=CONTROL_ZONE_FINISH)
    await callback.message.edit_text(CONTROL_ZONE_FINISH, reply_markup=control_zone_finish_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(ControlZoneSteps.finish), F.data == "control_zone_exit")
async def control_zone_finish_exit(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(CONTROL_ZONE_FINISH, parse_mode="HTML")
    await callback.message.answer("Вы завершили упражнение. Главное меню:", reply_markup=main_menu)
    streak_msg = process_streak(callback.from_user.id)
    if streak_msg:
        await callback.message.answer(streak_msg)
    await callback.answer()

@exercises_router.callback_query(StateFilter(ControlZoneSteps), F.data == "control_zone_exit")
async def exit_control_zone(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Упражнение прервано. Возвращаемся в главное меню.")
    await callback.message.answer("Главное меню", reply_markup=main_menu)
    await callback.answer()

@exercises_router.message(StateFilter(ControlZoneSteps), Command("cancel"))
async def cancel_control_zone(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Упражнение отменено. Главное меню:", reply_markup=main_menu)

# ===== Упражнение Самосострадание =====
@exercises_router.message(F.text == SELF_COMPASSION_BUTTON)
async def start_self_compassion(message: Message, state: FSMContext):
    await state.clear()
    logging.info(f"User {message.from_user.id} started Self-Compassion exercise")
    await state.set_state(SelfCompassionSteps.intro)
    await state.update_data(current_text=SELF_COMPASSION_INTRO)
    await message.answer(SELF_COMPASSION_INTRO, reply_markup=self_compassion_continue_keyboard(), parse_mode="HTML")

@exercises_router.callback_query(StateFilter(SelfCompassionSteps.intro), F.data == "self_compassion_next")
async def self_compassion_step_touch(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SelfCompassionSteps.touch)
    await state.update_data(current_text=SELF_COMPASSION_STEP_TOUCH)
    await callback.message.edit_text(SELF_COMPASSION_STEP_TOUCH, reply_markup=self_compassion_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(SelfCompassionSteps.touch), F.data == "self_compassion_next")
async def self_compassion_step_phrase1(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SelfCompassionSteps.phrase1)
    await state.update_data(current_text=SELF_COMPASSION_STEP_PHRASE1)
    await callback.message.edit_text(SELF_COMPASSION_STEP_PHRASE1, reply_markup=self_compassion_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(SelfCompassionSteps.phrase1), F.data == "self_compassion_next")
async def self_compassion_step_phrase2(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SelfCompassionSteps.phrase2)
    await state.update_data(current_text=SELF_COMPASSION_STEP_PHRASE2)
    await callback.message.edit_text(SELF_COMPASSION_STEP_PHRASE2, reply_markup=self_compassion_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(SelfCompassionSteps.phrase2), F.data == "self_compassion_next")
async def self_compassion_step_phrase3(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SelfCompassionSteps.phrase3)
    await state.update_data(current_text=SELF_COMPASSION_STEP_PHRASE3)
    await callback.message.edit_text(SELF_COMPASSION_STEP_PHRASE3, reply_markup=self_compassion_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(SelfCompassionSteps.phrase3), F.data == "self_compassion_next")
async def self_compassion_step_breathe(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SelfCompassionSteps.breathe)
    await state.update_data(current_text=SELF_COMPASSION_STEP_BREATHE)
    await callback.message.edit_text(SELF_COMPASSION_STEP_BREATHE, reply_markup=self_compassion_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(SelfCompassionSteps.breathe), F.data == "self_compassion_next")
async def self_compassion_step_finish(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SelfCompassionSteps.finish)
    await state.update_data(current_text=SELF_COMPASSION_FINISH)
    await callback.message.edit_text(SELF_COMPASSION_FINISH, reply_markup=self_compassion_finish_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(SelfCompassionSteps.finish), F.data == "self_compassion_exit")
async def self_compassion_finish_exit(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(SELF_COMPASSION_FINISH, parse_mode="HTML")
    await callback.message.answer("Вы завершили упражнение. Главное меню:", reply_markup=main_menu)
    streak_msg = process_streak(callback.from_user.id)
    if streak_msg:
        await callback.message.answer(streak_msg)
    await callback.answer()

@exercises_router.callback_query(StateFilter(SelfCompassionSteps), F.data == "self_compassion_exit")
async def exit_self_compassion(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Упражнение прервано. Возвращаемся в главное меню.")
    await callback.message.answer("Главное меню", reply_markup=main_menu)
    await callback.answer()

@exercises_router.message(StateFilter(SelfCompassionSteps), Command("cancel"))
async def cancel_self_compassion(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Упражнение отменено. Главное меню:", reply_markup=main_menu)

# ===== Упражнение Письмо без отправки =====
@exercises_router.message(F.text == UNSENT_LETTER_BUTTON)
async def start_unsent_letter(message: Message, state: FSMContext):
    await state.clear()
    logging.info(f"User {message.from_user.id} started Unsent Letter exercise")
    await state.set_state(UnsentLetterSteps.intro)
    await state.update_data(current_text=UNSENT_LETTER_INTRO)
    await message.answer(UNSENT_LETTER_INTRO, reply_markup=unsent_letter_continue_keyboard(), parse_mode="HTML")

@exercises_router.callback_query(StateFilter(UnsentLetterSteps.intro), F.data == "unsent_letter_next")
async def unsent_letter_step_to(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UnsentLetterSteps.to)
    await state.update_data(current_text=UNSENT_LETTER_STEP_TO)
    await callback.message.edit_text(UNSENT_LETTER_STEP_TO, reply_markup=unsent_letter_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(UnsentLetterSteps.to), F.data == "unsent_letter_next")
async def unsent_letter_step_emotion(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UnsentLetterSteps.emotion)
    await state.update_data(current_text=UNSENT_LETTER_STEP_EMOTION)
    await callback.message.edit_text(UNSENT_LETTER_STEP_EMOTION, reply_markup=unsent_letter_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(UnsentLetterSteps.emotion), F.data == "unsent_letter_next")
async def unsent_letter_step_say(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UnsentLetterSteps.say)
    await state.update_data(current_text=UNSENT_LETTER_STEP_SAY)
    await callback.message.edit_text(UNSENT_LETTER_STEP_SAY, reply_markup=unsent_letter_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(UnsentLetterSteps.say), F.data == "unsent_letter_next")
async def unsent_letter_step_need(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UnsentLetterSteps.need)
    await state.update_data(current_text=UNSENT_LETTER_STEP_NEED)
    await callback.message.edit_text(UNSENT_LETTER_STEP_NEED, reply_markup=unsent_letter_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(UnsentLetterSteps.need), F.data == "unsent_letter_next")
async def unsent_letter_step_finish(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UnsentLetterSteps.finish)
    await state.update_data(current_text=UNSENT_LETTER_FINISH)
    await callback.message.edit_text(UNSENT_LETTER_FINISH, reply_markup=unsent_letter_finish_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(UnsentLetterSteps.finish), F.data == "unsent_letter_exit")
async def unsent_letter_finish_exit(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(UNSENT_LETTER_FINISH, parse_mode="HTML")
    await callback.message.answer("Вы завершили упражнение. Главное меню:", reply_markup=main_menu)
    streak_msg = process_streak(callback.from_user.id)
    if streak_msg:
        await callback.message.answer(streak_msg)
    await callback.answer()

@exercises_router.callback_query(StateFilter(UnsentLetterSteps), F.data == "unsent_letter_exit")
async def exit_unsent_letter(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Упражнение прервано. Возвращаемся в главное меню.")
    await callback.message.answer("Главное меню", reply_markup=main_menu)
    await callback.answer()

@exercises_router.message(StateFilter(UnsentLetterSteps), Command("cancel"))
async def cancel_unsent_letter(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Упражнение отменено. Главное меню:", reply_markup=main_menu)

# ===== Дыхание 4–6 =====
@exercises_router.message(F.text == BREATHING_46_BUTTON)
async def start_breathing46(message: Message, state: FSMContext):
    await state.clear()
    logging.info(f"User {message.from_user.id} started Breathing 4-6")
    await state.set_state(Breathing46Steps.intro)
    await state.update_data(current_text=BREATHING_46_INTRO)
    await message.answer(BREATHING_46_INTRO, reply_markup=breathing46_continue_keyboard(), parse_mode="HTML")

@exercises_router.callback_query(StateFilter(Breathing46Steps.intro), F.data == "breathing46_next")
async def breathing46_step_inhale(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Breathing46Steps.inhale)
    await state.update_data(current_text=BREATHING_46_STEP_INHALE)
    await callback.message.edit_text(BREATHING_46_STEP_INHALE, reply_markup=breathing46_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(Breathing46Steps.inhale), F.data == "breathing46_next")
async def breathing46_step_exhale(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Breathing46Steps.exhale)
    await state.update_data(current_text=BREATHING_46_STEP_EXHALE)
    await callback.message.edit_text(BREATHING_46_STEP_EXHALE, reply_markup=breathing46_continue_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(Breathing46Steps.exhale), F.data == "breathing46_next")
async def breathing46_step_finish(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Breathing46Steps.finish)
    await state.update_data(current_text=BREATHING_46_FINISH)
    await callback.message.edit_text(BREATHING_46_FINISH, reply_markup=breathing46_finish_keyboard(), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(Breathing46Steps.finish), F.data == "breathing46_exit")
async def breathing46_finish_exit(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(BREATHING_46_FINISH, parse_mode="HTML")
    await callback.message.answer("Вы завершили упражнение. Главное меню:", reply_markup=main_menu)
    streak_msg = process_streak(callback.from_user.id)
    if streak_msg:
        await callback.message.answer(streak_msg)
    await callback.answer()

@exercises_router.callback_query(StateFilter(Breathing46Steps), F.data == "breathing46_exit")
async def exit_breathing46(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Упражнение прервано. Возвращаемся в главное меню.")
    await callback.message.answer("Главное меню", reply_markup=main_menu)
    await callback.answer()

@exercises_router.message(StateFilter(Breathing46Steps), Command("cancel"))
async def cancel_breathing46(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Упражнение отменено. Главное меню:", reply_markup=main_menu)