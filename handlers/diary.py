from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards import main_menu, diary_mode_keyboard, fast_mood_keyboard
from database import save_diary_entry, get_diary_stats, update_streak, get_streak
from texts import (
    STREAK_UPDATED_TEXT,
    STREAK_LEVEL_UP_TO_FLOWER,
    STREAK_LEVEL_UP_TO_TREE,
    FAST_MOOD_PROMPT,
    FAST_MOOD_SAVED,
    FAST_MOOD_EMOJI_MAP,
)

router = Router()

class DiaryStates(StatesGroup):
    choose_mode = State()
    mood = State()
    anxiety = State()
    energy = State()
    sleep = State()
    note = State()

cancel_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❌ Отмена")],
    ],
    resize_keyboard=True
)

sleep_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Плохо"),
            KeyboardButton(text="Нормально"),
            KeyboardButton(text="Хорошо"),
        ],
        [
            KeyboardButton(text="❌ Отмена"),
        ],
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
@router.message(F.text == "📝 Дневник")
async def start_diary(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(DiaryStates.choose_mode)
    await message.answer(
        "Выбери формат записи:",
        reply_markup=diary_mode_keyboard()
    )

@router.message(StateFilter(DiaryStates.choose_mode), F.text == "⚡ Быстрая отметка")
async def fast_mood_start(message: Message, state: FSMContext):
    await message.answer(FAST_MOOD_PROMPT, reply_markup=fast_mood_keyboard())
    await state.set_state(DiaryStates.mood)  # используем состояние mood, но для быстрой отметки

@router.message(StateFilter(DiaryStates.choose_mode), F.text == "📝 Полный дневник")
async def full_diary_start(message: Message, state: FSMContext):
    await message.answer(
        "Давай сделаем короткую запись в дневник.\n\n"
        "Это займёт около минуты.\n\n"
        "Первый вопрос:\n\n"
        "Какое сейчас настроение от 1 до 10?\n\n"
        "1 — очень плохо\n"
        "10 — очень хорошо",
        reply_markup=cancel_menu
    )
    await state.set_state(DiaryStates.mood)

@router.callback_query(StateFilter(DiaryStates.mood), F.data.startswith("fast_mood_"))
async def fast_mood_callback(callback: CallbackQuery, state: FSMContext):
    emoji_text = callback.data[len("fast_mood_"):]
    mood_score = FAST_MOOD_EMOJI_MAP.get(emoji_text, 5)
    telegram_id = callback.from_user.id

    # Сохраняем запись дневника с этой эмоцией
    save_diary_entry(
        telegram_id=telegram_id,
        mood_score=mood_score,
        anxiety_score=None,
        energy_score=None,
        sleep_quality=None,
        note=emoji_text,
    )

    await state.clear()
    await callback.message.edit_text(FAST_MOOD_SAVED)
    await callback.answer("Сохранено!")

    # Стрик
    update_streak(telegram_id)
    streak_data = get_streak(telegram_id)
    if streak_data["current_streak"] == 30:
        await callback.message.answer(STREAK_LEVEL_UP_TO_TREE)
    elif streak_data["current_streak"] == 7:
        await callback.message.answer(STREAK_LEVEL_UP_TO_FLOWER)
    else:
        await callback.message.answer(STREAK_UPDATED_TEXT.format(streak=streak_data["current_streak"]))

    await callback.message.answer("Главное меню", reply_markup=main_menu)

@router.message(StateFilter(DiaryStates.mood))
async def diary_mood(message: Message, state: FSMContext):
    # Проверяем, не быстрая ли отметка (текст кнопки)
    if message.text in [key for key in FAST_MOOD_EMOJI_MAP.keys()]:
        # Игнорируем текстовые кнопки, они обрабатываются callback
        return

    score = parse_score(message.text or "")
    if score is None:
        await message.answer("Пожалуйста, напиши число от 1 до 10.\n\nНапример: 6")
        return

    await state.update_data(mood_score=score)
    await message.answer(
        "Спасибо.\n\n"
        "Теперь оцени тревогу от 1 до 10.\n\n"
        "1 — почти нет тревоги\n"
        "10 — очень сильная тревога"
    )
    await state.set_state(DiaryStates.anxiety)

# ... остальные обработчики (anxiety, energy, sleep, note) без изменений

@router.message(StateFilter(DiaryStates.anxiety))
async def diary_anxiety(message: Message, state: FSMContext):
    score = parse_score(message.text or "")
    if score is None:
        await message.answer("Пожалуйста, напиши число от 1 до 10.\n\nНапример: 7")
        return
    await state.update_data(anxiety_score=score)
    await message.answer("Понял.\n\nТеперь энергия от 1 до 10.\n\n1 — совсем нет сил\n10 — много энергии")
    await state.set_state(DiaryStates.energy)

@router.message(StateFilter(DiaryStates.energy))
async def diary_energy(message: Message, state: FSMContext):
    score = parse_score(message.text or "")
    if score is None:
        await message.answer("Пожалуйста, напиши число от 1 до 10.\n\nНапример: 4")
        return
    await state.update_data(energy_score=score)
    await message.answer("Как ты спал/спала?", reply_markup=sleep_menu)
    await state.set_state(DiaryStates.sleep)

@router.message(StateFilter(DiaryStates.sleep))
async def diary_sleep(message: Message, state: FSMContext):
    sleep_quality = (message.text or "").strip().lower()
    allowed = ["плохо", "нормально", "хорошо"]
    if sleep_quality not in allowed:
        await message.answer("Выбери один из вариантов:\n\nПлохо / Нормально / Хорошо", reply_markup=sleep_menu)
        return
    await state.update_data(sleep_quality=sleep_quality)
    await message.answer(
        "Последний вопрос.\n\n"
        "Что сегодня сильнее всего повлияло на твоё состояние?\n\n"
        "Можно коротко: событие, мысль, разговор, усталость, конфликт, ожидание и т.д.",
        reply_markup=cancel_menu
    )
    await state.set_state(DiaryStates.note)

@router.message(StateFilter(DiaryStates.note))
async def diary_note(message: Message, state: FSMContext):
    note = (message.text or "").strip()
    if not note:
        await message.answer("Напиши хотя бы пару слов.\n\nНапример: «много работы», «ссора», «не ответил человек», «плохо спала».")
        return

    data = await state.get_data()
    telegram_id = message.from_user.id if message.from_user else 0

    save_diary_entry(
        telegram_id=telegram_id,
        mood_score=data.get("mood_score"),
        anxiety_score=data.get("anxiety_score"),
        energy_score=data.get("energy_score"),
        sleep_quality=data.get("sleep_quality"),
        note=note,
    )

    await state.clear()

    mood = data.get("mood_score")
    anxiety = data.get("anxiety_score")
    energy = data.get("energy_score")
    sleep_quality = data.get("sleep_quality")

    response = (
        "Готово. Я сохранил запись в дневник 📝\n\n"
        f"Настроение: {mood}/10\n"
        f"Тревога: {anxiety}/10\n"
        f"Энергия: {energy}/10\n"
        f"Сон: {sleep_quality}\n"
        f"Что повлияло: {note}\n\n"
    )
    if anxiety and anxiety >= 7:
        response += "Вижу, тревога довольно высокая. Если хочешь, можно сейчас нажать 🆘 «Меня накрыло» и сделать короткое упражнение.\n\n"
    if energy and energy <= 3:
        response += "Похоже, энергии мало. Сегодня лучше не требовать от себя максимума — выбери один самый маленький обязательный шаг.\n\n"
    response += "Хочешь посмотреть краткую статистику дневника? Напиши /diary_stats"

    await message.answer(response, reply_markup=main_menu)

    # Стрик
    update_streak(telegram_id)
    streak_data = get_streak(telegram_id)
    if streak_data["current_streak"] == 30:
        await message.answer(STREAK_LEVEL_UP_TO_TREE)
    elif streak_data["current_streak"] == 7:
        await message.answer(STREAK_LEVEL_UP_TO_FLOWER)
    else:
        await message.answer(STREAK_UPDATED_TEXT.format(streak=streak_data["current_streak"]))

# Команда /diary_stats остаётся без изменений
@router.message(Command("diary_stats"))
async def diary_stats_command(message: Message):
    if not message.from_user:
        await message.answer("Не смог определить пользователя.")
        return
    stats = get_diary_stats(message.from_user.id)
    if not stats:
        await message.answer(
            "Пока нет записей в дневнике.\n\nНажми 📝 Дневник или напиши /diary, чтобы создать первую запись.",
            reply_markup=main_menu
        )
        return
    await message.answer(
        "Краткая статистика дневника:\n\n"
        f"Записей: {stats['count']}\n"
        f"Среднее настроение: {stats['avg_mood']}/10\n"
        f"Средняя тревога: {stats['avg_anxiety']}/10\n"
        f"Средняя энергия: {stats['avg_energy']}/10\n\n"
        "Это пока простая статистика. Позже на её основе мы сделаем «Мою карту».",
        reply_markup=main_menu
    )