import logging, re, tempfile, os
from gtts import gTTS
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command, StateFilter
from aiogram.enums import ChatAction

from keyboards import (
    breathing_continue_keyboard, breathing_finish_keyboard,
    grounding_continue_keyboard, grounding_finish_keyboard,
    stop_continue_keyboard, stop_finish_keyboard,
    control_zone_continue_keyboard, control_zone_finish_keyboard,
    self_compassion_continue_keyboard, self_compassion_finish_keyboard,
    unsent_letter_continue_keyboard, unsent_letter_finish_keyboard,
    breathing46_continue_keyboard, breathing46_finish_keyboard,
    get_main_menu, get_exercises_menu,
)
from services.streak_service import process_streak
from services.i18n import get_text

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

def clean_html(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text).strip()

def get_lang(kwargs):
    return kwargs.get("lang", "ru")

@exercises_router.callback_query(F.data == "listen")
async def listen_step(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("current_text")
    if not text:
        text = callback.message.text or callback.message.caption or ""
        text = clean_html(text)
    else:
        text = clean_html(text)
    if not text:
        await callback.answer("Nothing to read.")
        return
    await callback.answer("Generating audio...")
    await callback.bot.send_chat_action(chat_id=callback.message.chat.id, action=ChatAction.RECORD_VOICE)
    audio_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tts = gTTS(text=text, lang="ru")
            tts.save(f.name)
            audio_path = f.name
        await callback.message.answer_audio(FSInputFile(audio_path, filename="instruction.mp3"), title="Instruction")
    except Exception as e:
        logging.exception("TTS failed")
        await callback.message.answer("Failed to create audio. Try later.")
    finally:
        if audio_path and os.path.exists(audio_path):
            os.unlink(audio_path)

# ===== Дыхание по квадрату =====
@exercises_router.message(F.text.in_([get_text("breathing_button", "ru"), get_text("breathing_button", "en")]))
async def start_breathing(message: Message, state: FSMContext, **kwargs):
    await state.clear()
    lang = get_lang(kwargs)
    await state.set_state(BreathingSteps.intro)
    text = get_text("breathing_intro", lang)
    await state.update_data(current_text=text)
    await message.answer(text, reply_markup=breathing_continue_keyboard(lang))

@exercises_router.callback_query(F.data == "breathing_next")
async def next_step(callback: CallbackQuery, state: FSMContext, **kwargs):
    current_state = await state.get_state()
    lang = get_lang(kwargs)
    if current_state == BreathingSteps.intro.state:
        await state.set_state(BreathingSteps.inhale)
        text = get_text("breathing_step_inhale", lang)
    elif current_state == BreathingSteps.inhale.state:
        await state.set_state(BreathingSteps.hold_in)
        text = get_text("breathing_step_hold_in", lang)
    elif current_state == BreathingSteps.hold_in.state:
        await state.set_state(BreathingSteps.exhale)
        text = get_text("breathing_step_exhale", lang)
    elif current_state == BreathingSteps.exhale.state:
        await state.set_state(BreathingSteps.hold_out)
        text = get_text("breathing_step_hold_out", lang)
    elif current_state == BreathingSteps.hold_out.state:
        await state.set_state(BreathingSteps.finish)
        text = get_text("breathing_finish", lang)
    else:
        await exit_breathing(callback, state)
        return
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=breathing_continue_keyboard(lang))
    await callback.answer()

@exercises_router.callback_query(F.data == "breathing_exit")
async def exit_breathing(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.clear()
    await callback.message.edit_text(get_text("back_to_main_menu", lang))
    await callback.message.answer(get_text("back_to_main_menu", lang), reply_markup=get_main_menu(lang))
    await callback.answer()

# ===== 5-4-3-2-1 =====
@exercises_router.message(F.text.in_([get_text("grounding_button", "ru"), get_text("grounding_button", "en")]))
async def start_grounding(message: Message, state: FSMContext, **kwargs):
    await state.clear()
    lang = get_lang(kwargs)
    await state.set_state(GroundingSteps.intro)
    text = get_text("grounding_intro", lang)
    await state.update_data(current_text=text)
    await message.answer(text, reply_markup=grounding_continue_keyboard(lang), parse_mode="HTML")

@exercises_router.callback_query(StateFilter(GroundingSteps.intro), F.data == "grounding_next")
async def grounding_step_see(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(GroundingSteps.see)
    text = get_text("grounding_step_see", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=grounding_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps.see), F.data == "grounding_next")
async def grounding_step_touch(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(GroundingSteps.touch)
    text = get_text("grounding_step_touch", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=grounding_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps.touch), F.data == "grounding_next")
async def grounding_step_hear(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(GroundingSteps.hear)
    text = get_text("grounding_step_hear", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=grounding_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps.hear), F.data == "grounding_next")
async def grounding_step_smell(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(GroundingSteps.smell)
    text = get_text("grounding_step_smell", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=grounding_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps.smell), F.data == "grounding_next")
async def grounding_step_taste(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(GroundingSteps.taste)
    text = get_text("grounding_step_taste", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=grounding_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps.taste), F.data == "grounding_next")
async def grounding_step_finish(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(GroundingSteps.finish)
    text = get_text("grounding_finish", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=grounding_finish_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps.finish), F.data == "grounding_exit")
async def grounding_finish_exit(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.clear()
    await callback.message.edit_text(get_text("grounding_finish", lang), parse_mode="HTML")
    await callback.message.answer(get_text("exercise_completed", lang), reply_markup=get_main_menu(lang))
    streak_msg = process_streak(callback.from_user.id)
    if streak_msg:
        await callback.message.answer(streak_msg)
    await callback.answer()

@exercises_router.callback_query(StateFilter(GroundingSteps), F.data == "grounding_exit")
async def exit_grounding(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.clear()
    await callback.message.edit_text(get_text("exercise_cancelled", lang))
    await callback.message.answer(get_text("back_to_main_menu", lang), reply_markup=get_main_menu(lang))
    await callback.answer()

# ===== STOP =====
@exercises_router.message(F.text.in_([get_text("stop_button", "ru"), get_text("stop_button", "en")]))
async def start_stop(message: Message, state: FSMContext, **kwargs):
    await state.clear()
    lang = get_lang(kwargs)
    await state.set_state(StopSteps.intro)
    text = get_text("stop_intro", lang)
    await state.update_data(current_text=text)
    await message.answer(text, reply_markup=stop_continue_keyboard(lang), parse_mode="HTML")

@exercises_router.callback_query(StateFilter(StopSteps.intro), F.data == "stop_next")
async def stop_step_stop(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(StopSteps.stop)
    text = get_text("stop_step_stop", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=stop_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(StopSteps.stop), F.data == "stop_next")
async def stop_step_breathe(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(StopSteps.breathe)
    text = get_text("stop_step_breathe", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=stop_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(StopSteps.breathe), F.data == "stop_next")
async def stop_step_observe(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(StopSteps.observe)
    text = get_text("stop_step_observe", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=stop_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(StopSteps.observe), F.data == "stop_next")
async def stop_step_proceed(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(StopSteps.proceed)
    text = get_text("stop_step_proceed", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=stop_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(StopSteps.proceed), F.data == "stop_next")
async def stop_step_finish(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(StopSteps.finish)
    text = get_text("stop_finish", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=stop_finish_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(StopSteps.finish), F.data == "stop_exit")
async def stop_finish_exit(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.clear()
    await callback.message.edit_text(get_text("stop_finish", lang), parse_mode="HTML")
    await callback.message.answer(get_text("exercise_completed", lang), reply_markup=get_main_menu(lang))
    streak_msg = process_streak(callback.from_user.id)
    if streak_msg:
        await callback.message.answer(streak_msg)
    await callback.answer()

@exercises_router.callback_query(StateFilter(StopSteps), F.data == "stop_exit")
async def exit_stop(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.clear()
    await callback.message.edit_text(get_text("exercise_cancelled", lang))
    await callback.message.answer(get_text("back_to_main_menu", lang), reply_markup=get_main_menu(lang))
    await callback.answer()

# ===== Зона контроля =====
@exercises_router.message(F.text.in_([get_text("control_zone_button", "ru"), get_text("control_zone_button", "en")]))
async def start_control_zone(message: Message, state: FSMContext, **kwargs):
    await state.clear()
    lang = get_lang(kwargs)
    await state.set_state(ControlZoneSteps.intro)
    text = get_text("control_zone_intro", lang)
    await state.update_data(current_text=text)
    await message.answer(text, reply_markup=control_zone_continue_keyboard(lang), parse_mode="HTML")

@exercises_router.callback_query(StateFilter(ControlZoneSteps.intro), F.data == "control_zone_next")
async def control_zone_step_out(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(ControlZoneSteps.out_of_control)
    text = get_text("control_zone_step_out", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=control_zone_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(ControlZoneSteps.out_of_control), F.data == "control_zone_next")
async def control_zone_step_influence(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(ControlZoneSteps.influence)
    text = get_text("control_zone_step_influence", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=control_zone_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(ControlZoneSteps.influence), F.data == "control_zone_next")
async def control_zone_step_action(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(ControlZoneSteps.action)
    text = get_text("control_zone_step_action", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=control_zone_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(ControlZoneSteps.action), F.data == "control_zone_next")
async def control_zone_step_finish(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(ControlZoneSteps.finish)
    text = get_text("control_zone_finish", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=control_zone_finish_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(ControlZoneSteps.finish), F.data == "control_zone_exit")
async def control_zone_finish_exit(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.clear()
    await callback.message.edit_text(get_text("control_zone_finish", lang), parse_mode="HTML")
    await callback.message.answer(get_text("exercise_completed", lang), reply_markup=get_main_menu(lang))
    streak_msg = process_streak(callback.from_user.id)
    if streak_msg:
        await callback.message.answer(streak_msg)
    await callback.answer()

@exercises_router.callback_query(StateFilter(ControlZoneSteps), F.data == "control_zone_exit")
async def exit_control_zone(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.clear()
    await callback.message.edit_text(get_text("exercise_cancelled", lang))
    await callback.message.answer(get_text("back_to_main_menu", lang), reply_markup=get_main_menu(lang))
    await callback.answer()

# ===== Самосострадание =====
@exercises_router.message(F.text.in_([get_text("self_compassion_button", "ru"), get_text("self_compassion_button", "en")]))
async def start_self_compassion(message: Message, state: FSMContext, **kwargs):
    await state.clear()
    lang = get_lang(kwargs)
    await state.set_state(SelfCompassionSteps.intro)
    text = get_text("self_compassion_intro", lang)
    await state.update_data(current_text=text)
    await message.answer(text, reply_markup=self_compassion_continue_keyboard(lang), parse_mode="HTML")

@exercises_router.callback_query(StateFilter(SelfCompassionSteps.intro), F.data == "self_compassion_next")
async def self_compassion_step_touch(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(SelfCompassionSteps.touch)
    text = get_text("self_compassion_step_touch", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=self_compassion_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(SelfCompassionSteps.touch), F.data == "self_compassion_next")
async def self_compassion_step_phrase1(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(SelfCompassionSteps.phrase1)
    text = get_text("self_compassion_step_phrase1", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=self_compassion_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(SelfCompassionSteps.phrase1), F.data == "self_compassion_next")
async def self_compassion_step_phrase2(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(SelfCompassionSteps.phrase2)
    text = get_text("self_compassion_step_phrase2", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=self_compassion_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(SelfCompassionSteps.phrase2), F.data == "self_compassion_next")
async def self_compassion_step_phrase3(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(SelfCompassionSteps.phrase3)
    text = get_text("self_compassion_step_phrase3", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=self_compassion_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(SelfCompassionSteps.phrase3), F.data == "self_compassion_next")
async def self_compassion_step_breathe(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(SelfCompassionSteps.breathe)
    text = get_text("self_compassion_step_breathe", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=self_compassion_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(SelfCompassionSteps.breathe), F.data == "self_compassion_next")
async def self_compassion_step_finish(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(SelfCompassionSteps.finish)
    text = get_text("self_compassion_finish", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=self_compassion_finish_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(SelfCompassionSteps.finish), F.data == "self_compassion_exit")
async def self_compassion_finish_exit(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.clear()
    await callback.message.edit_text(get_text("self_compassion_finish", lang), parse_mode="HTML")
    await callback.message.answer(get_text("exercise_completed", lang), reply_markup=get_main_menu(lang))
    streak_msg = process_streak(callback.from_user.id)
    if streak_msg:
        await callback.message.answer(streak_msg)
    await callback.answer()

@exercises_router.callback_query(StateFilter(SelfCompassionSteps), F.data == "self_compassion_exit")
async def exit_self_compassion(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.clear()
    await callback.message.edit_text(get_text("exercise_cancelled", lang))
    await callback.message.answer(get_text("back_to_main_menu", lang), reply_markup=get_main_menu(lang))
    await callback.answer()

# ===== Письмо без отправки =====
@exercises_router.message(F.text.in_([get_text("unsent_letter_button", "ru"), get_text("unsent_letter_button", "en")]))
async def start_unsent_letter(message: Message, state: FSMContext, **kwargs):
    await state.clear()
    lang = get_lang(kwargs)
    await state.set_state(UnsentLetterSteps.intro)
    text = get_text("unsent_letter_intro", lang)
    await state.update_data(current_text=text)
    await message.answer(text, reply_markup=unsent_letter_continue_keyboard(lang), parse_mode="HTML")

@exercises_router.callback_query(StateFilter(UnsentLetterSteps.intro), F.data == "unsent_letter_next")
async def unsent_letter_step_to(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(UnsentLetterSteps.to)
    text = get_text("unsent_letter_step_to", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=unsent_letter_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(UnsentLetterSteps.to), F.data == "unsent_letter_next")
async def unsent_letter_step_emotion(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(UnsentLetterSteps.emotion)
    text = get_text("unsent_letter_step_emotion", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=unsent_letter_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(UnsentLetterSteps.emotion), F.data == "unsent_letter_next")
async def unsent_letter_step_say(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(UnsentLetterSteps.say)
    text = get_text("unsent_letter_step_say", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=unsent_letter_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(UnsentLetterSteps.say), F.data == "unsent_letter_next")
async def unsent_letter_step_need(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(UnsentLetterSteps.need)
    text = get_text("unsent_letter_step_need", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=unsent_letter_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(UnsentLetterSteps.need), F.data == "unsent_letter_next")
async def unsent_letter_step_finish(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(UnsentLetterSteps.finish)
    text = get_text("unsent_letter_finish", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=unsent_letter_finish_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(UnsentLetterSteps.finish), F.data == "unsent_letter_exit")
async def unsent_letter_finish_exit(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.clear()
    await callback.message.edit_text(get_text("unsent_letter_finish", lang), parse_mode="HTML")
    await callback.message.answer(get_text("exercise_completed", lang), reply_markup=get_main_menu(lang))
    streak_msg = process_streak(callback.from_user.id)
    if streak_msg:
        await callback.message.answer(streak_msg)
    await callback.answer()

@exercises_router.callback_query(StateFilter(UnsentLetterSteps), F.data == "unsent_letter_exit")
async def exit_unsent_letter(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.clear()
    await callback.message.edit_text(get_text("exercise_cancelled", lang))
    await callback.message.answer(get_text("back_to_main_menu", lang), reply_markup=get_main_menu(lang))
    await callback.answer()

# ===== Дыхание 4–6 =====
@exercises_router.message(F.text.in_([get_text("breathing_46_button", "ru"), get_text("breathing_46_button", "en")]))
async def start_breathing46(message: Message, state: FSMContext, **kwargs):
    await state.clear()
    lang = get_lang(kwargs)
    await state.set_state(Breathing46Steps.intro)
    text = get_text("breathing_46_intro", lang)
    await state.update_data(current_text=text)
    await message.answer(text, reply_markup=breathing46_continue_keyboard(lang), parse_mode="HTML")

@exercises_router.callback_query(StateFilter(Breathing46Steps.intro), F.data == "breathing46_next")
async def breathing46_step_inhale(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(Breathing46Steps.inhale)
    text = get_text("breathing_46_step_inhale", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=breathing46_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(Breathing46Steps.inhale), F.data == "breathing46_next")
async def breathing46_step_exhale(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(Breathing46Steps.exhale)
    text = get_text("breathing_46_step_exhale", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=breathing46_continue_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(Breathing46Steps.exhale), F.data == "breathing46_next")
async def breathing46_step_finish(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.set_state(Breathing46Steps.finish)
    text = get_text("breathing_46_finish", lang)
    await state.update_data(current_text=text)
    await callback.message.edit_text(text, reply_markup=breathing46_finish_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@exercises_router.callback_query(StateFilter(Breathing46Steps.finish), F.data == "breathing46_exit")
async def breathing46_finish_exit(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.clear()
    await callback.message.edit_text(get_text("breathing_46_finish", lang), parse_mode="HTML")
    await callback.message.answer(get_text("exercise_completed", lang), reply_markup=get_main_menu(lang))
    streak_msg = process_streak(callback.from_user.id)
    if streak_msg:
        await callback.message.answer(streak_msg)
    await callback.answer()

@exercises_router.callback_query(StateFilter(Breathing46Steps), F.data == "breathing46_exit")
async def exit_breathing46(callback: CallbackQuery, state: FSMContext, **kwargs):
    lang = get_lang(kwargs)
    await state.clear()
    await callback.message.edit_text(get_text("exercise_cancelled", lang))
    await callback.message.answer(get_text("back_to_main_menu", lang), reply_markup=get_main_menu(lang))
    await callback.answer()