from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from keyboards import get_main_menu, diary_mode_keyboard, fast_mood_keyboard
from services.diary_service import save_and_process_diary_entry, get_diary_stats_message
from services.i18n import get_text

router = Router()

class DiaryStates(StatesGroup):
    choose_mode = State()
    mood = State()
    anxiety = State()
    energy = State()
    sleep = State()
    note = State()

def get_cancel_menu(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=get_text("cancel_button", lang))]],
        resize_keyboard=True
    )

def get_sleep_menu(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_text("sleep_bad", lang)),
                KeyboardButton(text=get_text("sleep_ok", lang)),
                KeyboardButton(text=get_text("sleep_good", lang)),
            ],
            [KeyboardButton(text=get_text("cancel_button", lang))],
        ],
        resize_keyboard=True
    )

def parse_score(text: str) -> int | None:
    try:
        value = int(text.strip())
    except ValueError:
        return None
    if 1 <= value <= 10:
        return value
    return None

@router.message(Command("diary"))
@router.message(F.text.in_([get_text("diary_button_text", "ru"), get_text("diary_button_text", "en")]))
async def start_diary(message: Message, state: FSMContext, **kwargs):
    await state.clear()
    await state.set_state(DiaryStates.choose_mode)
    lang = kwargs.get("lang", "ru")
    await message.answer(
        get_text("diary_choose_mode", lang),
        reply_markup=diary_mode_keyboard()
    )

@router.message(StateFilter(DiaryStates.choose_mode), F.text.in_([get_text("fast_mood_button", "ru"), get_text("fast_mood_button", "en")]))
async def fast_mood_start(message: Message, state: FSMContext, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("fast_mood_prompt", lang), reply_markup=fast_mood_keyboard())
    await state.set_state(DiaryStates.mood)

@router.message(StateFilter(DiaryStates.choose_mode), F.text.in_([get_text("full_diary_button", "ru"), get_text("full_diary_button", "en")]))
async def full_diary_start(message: Message, state: FSMContext, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(
        get_text("diary_full_start", lang),
        reply_markup=get_cancel_menu(lang)
    )
    await state.set_state(DiaryStates.mood)

@router.callback_query(StateFilter(DiaryStates.mood), F.data.startswith("fast_mood_"))
async def fast_mood_callback(callback: CallbackQuery, state: FSMContext, **kwargs):
    emoji_text = callback.data[len("fast_mood_"):]
    mood_score = get_text("fast_mood_emoji_map", "ru").get(emoji_text, 5)
    telegram_id = callback.from_user.id
    lang = kwargs.get("lang", "ru")

    _, streak_message = save_and_process_diary_entry(
        telegram_id=telegram_id,
        mood_score=mood_score,
        note=emoji_text,
    )

    await state.clear()
    await callback.message.edit_text(get_text("fast_mood_saved", lang))
    await callback.answer(get_text("fast_mood_saved", lang))

    if streak_message:
        await callback.message.answer(streak_message, reply_markup=get_main_menu(lang))
    else:
        await callback.message.answer(get_text("back_to_main_menu", lang), reply_markup=get_main_menu(lang))

@router.message(StateFilter(DiaryStates.mood))
async def diary_mood(message: Message, state: FSMContext, **kwargs):
    if message.text in get_text("fast_mood_emoji_map", "ru"):
        return

    score = parse_score(message.text or "")
    if score is None:
        lang = kwargs.get("lang", "ru")
        await message.answer(get_text("diary_score_prompt", lang))
        return

    await state.update_data(mood_score=score)
    lang = kwargs.get("lang", "ru")
    await message.answer(
        get_text("diary_anxiety_prompt", lang)
    )
    await state.set_state(DiaryStates.anxiety)

@router.message(StateFilter(DiaryStates.anxiety))
async def diary_anxiety(message: Message, state: FSMContext, **kwargs):
    score = parse_score(message.text or "")
    if score is None:
        lang = kwargs.get("lang", "ru")
        await message.answer(get_text("diary_score_prompt", lang))
        return
    await state.update_data(anxiety_score=score)
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("diary_energy_prompt", lang))
    await state.set_state(DiaryStates.energy)

@router.message(StateFilter(DiaryStates.energy))
async def diary_energy(message: Message, state: FSMContext, **kwargs):
    score = parse_score(message.text or "")
    if score is None:
        lang = kwargs.get("lang", "ru")
        await message.answer(get_text("diary_score_prompt", lang))
        return
    await state.update_data(energy_score=score)
    lang = kwargs.get("lang", "ru")
    await message.answer(get_text("diary_sleep_prompt", lang), reply_markup=get_sleep_menu(lang))
    await state.set_state(DiaryStates.sleep)

@router.message(StateFilter(DiaryStates.sleep))
async def diary_sleep(message: Message, state: FSMContext, **kwargs):
    lang = kwargs.get("lang", "ru")
    sleep_quality = (message.text or "").strip().lower()
    allowed = [
        get_text("sleep_bad", lang).lower(),
        get_text("sleep_ok", lang).lower(),
        get_text("sleep_good", lang).lower(),
    ]
    if sleep_quality not in allowed:
        await message.answer(get_text("diary_sleep_invalid", lang), reply_markup=get_sleep_menu(lang))
        return
    await state.update_data(sleep_quality=sleep_quality)
    await message.answer(
        get_text("diary_note_prompt", lang),
        reply_markup=get_cancel_menu(lang)
    )
    await state.set_state(DiaryStates.note)

@router.message(StateFilter(DiaryStates.note))
async def diary_note(message: Message, state: FSMContext, **kwargs):
    note = (message.text or "").strip()
    lang = kwargs.get("lang", "ru")
    if not note:
        await message.answer(get_text("diary_note_empty", lang))
        return

    data = await state.get_data()
    telegram_id = message.from_user.id if message.from_user else 0

    mood = data.get("mood_score")
    anxiety = data.get("anxiety_score")
    energy = data.get("energy_score")
    sleep_quality = data.get("sleep_quality")

    _, streak_message = save_and_process_diary_entry(
        telegram_id=telegram_id,
        mood_score=mood,
        anxiety_score=anxiety,
        energy_score=energy,
        sleep_quality=sleep_quality,
        note=note,
    )

    await state.clear()

    response = get_text("diary_saved", lang).format(
        mood=mood,
        anxiety=anxiety,
        energy=energy,
        sleep_quality=sleep_quality,
        note=note
    )

    if anxiety and anxiety >= 7:
        response += "\n\n" + get_text("diary_high_anxiety_note", lang)
    if energy and energy <= 3:
        response += "\n\n" + get_text("diary_low_energy_note", lang)
    response += "\n\n" + get_text("diary_suggest_stats", lang)

    await message.answer(response, reply_markup=get_main_menu(lang))

    if streak_message:
        await message.answer(streak_message)

@router.message(Command("diary_stats"))
async def diary_stats_command(message: Message, **kwargs):
    if not message.from_user:
        await message.answer("Не смог определить пользователя.")
        return
    lang = kwargs.get("lang", "ru")
    msg = get_diary_stats_message(message.from_user.id)
    await message.answer(msg, reply_markup=get_main_menu(lang))