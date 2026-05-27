from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from keyboards import main_menu
from database import save_diary_entry, get_diary_stats, update_streak, get_streak
from texts import STREAK_UPDATED_TEXT, STREAK_LEVEL_UP_TO_FLOWER, STREAK_LEVEL_UP_TO_TREE


router = Router()


class DiaryStates(StatesGroup):
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


@router.message(StateFilter(DiaryStates.mood, DiaryStates.anxiety, DiaryStates.energy, DiaryStates.sleep, DiaryStates.note), Command("cancel"))
@router.message(StateFilter(DiaryStates.mood, DiaryStates.anxiety, DiaryStates.energy, DiaryStates.sleep, DiaryStates.note), F.text == "❌ Отмена")
async def cancel_diary(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Ок, я отменил текущий сценарий.",
        reply_markup=main_menu
    )


@router.message(Command("diary"))
@router.message(F.text == "📝 Дневник")
async def start_diary(message: Message, state: FSMContext):
    await state.clear()

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


@router.message(DiaryStates.mood)
async def diary_mood(message: Message, state: FSMContext):
    score = parse_score(message.text or "")

    if score is None:
        await message.answer(
            "Пожалуйста, напиши число от 1 до 10.\n\n"
            "Например: 6"
        )
        return

    await state.update_data(mood_score=score)

    await message.answer(
        "Спасибо.\n\n"
        "Теперь оцени тревогу от 1 до 10.\n\n"
        "1 — почти нет тревоги\n"
        "10 — очень сильная тревога"
    )

    await state.set_state(DiaryStates.anxiety)


@router.message(DiaryStates.anxiety)
async def diary_anxiety(message: Message, state: FSMContext):
    score = parse_score(message.text or "")

    if score is None:
        await message.answer(
            "Пожалуйста, напиши число от 1 до 10.\n\n"
            "Например: 7"
        )
        return

    await state.update_data(anxiety_score=score)

    await message.answer(
        "Понял.\n\n"
        "Теперь энергия от 1 до 10.\n\n"
        "1 — совсем нет сил\n"
        "10 — много энергии"
    )

    await state.set_state(DiaryStates.energy)


@router.message(DiaryStates.energy)
async def diary_energy(message: Message, state: FSMContext):
    score = parse_score(message.text or "")

    if score is None:
        await message.answer(
            "Пожалуйста, напиши число от 1 до 10.\n\n"
            "Например: 4"
        )
        return

    await state.update_data(energy_score=score)

    await message.answer(
        "Как ты спал/спала?",
        reply_markup=sleep_menu
    )

    await state.set_state(DiaryStates.sleep)


@router.message(DiaryStates.sleep)
async def diary_sleep(message: Message, state: FSMContext):
    sleep_quality = (message.text or "").strip().lower()

    allowed = ["плохо", "нормально", "хорошо"]

    if sleep_quality not in allowed:
        await message.answer(
            "Выбери один из вариантов:\n\n"
            "Плохо / Нормально / Хорошо",
            reply_markup=sleep_menu
        )
        return

    await state.update_data(sleep_quality=sleep_quality)

    await message.answer(
        "Последний вопрос.\n\n"
        "Что сегодня сильнее всего повлияло на твоё состояние?\n\n"
        "Можно коротко: событие, мысль, разговор, усталость, конфликт, ожидание и т.д.",
        reply_markup=cancel_menu
    )

    await state.set_state(DiaryStates.note)


@router.message(DiaryStates.note)
async def diary_note(message: Message, state: FSMContext):
    note = (message.text or "").strip()

    if not note:
        await message.answer(
            "Напиши хотя бы пару слов.\n\n"
            "Например: «много работы», «ссора», «не ответил человек», «плохо спала»."
        )
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
        response += (
            "Вижу, тревога довольно высокая. "
            "Если хочешь, можно сейчас нажать 🆘 «Меня накрыло» и сделать короткое упражнение.\n\n"
        )

    if energy and energy <= 3:
        response += (
            "Похоже, энергии мало. Сегодня лучше не требовать от себя максимума — "
            "выбери один самый маленький обязательный шаг.\n\n"
        )

    response += "Хочешь посмотреть краткую статистику дневника? Напиши /diary_stats"

    await message.answer(response, reply_markup=main_menu)

    # Обновляем стрик
    update_streak(telegram_id)
    streak_data = get_streak(telegram_id)
    if streak_data["current_streak"] == 30:
        await message.answer(STREAK_LEVEL_UP_TO_TREE)
    elif streak_data["current_streak"] == 7:
        await message.answer(STREAK_LEVEL_UP_TO_FLOWER)
    else:
        await message.answer(STREAK_UPDATED_TEXT.format(streak=streak_data["current_streak"]))


@router.message(Command("diary_stats"))
async def diary_stats_command(message: Message):
    if not message.from_user:
        await message.answer("Не смог определить пользователя.")
        return

    stats = get_diary_stats(message.from_user.id)

    if not stats:
        await message.answer(
            "Пока нет записей в дневнике.\n\n"
            "Нажми 📝 Дневник или напиши /diary, чтобы создать первую запись.",
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