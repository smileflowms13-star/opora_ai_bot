from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from keyboards import main_menu
from database import save_trigger_entry, get_trigger_count, update_streak, get_streak
from texts import STREAK_UPDATED_TEXT, STREAK_LEVEL_UP_TO_FLOWER, STREAK_LEVEL_UP_TO_TREE


router = Router()


class TriggerStates(StatesGroup):
    situation = State()
    thought = State()
    emotion = State()
    body_reaction = State()
    impulse = State()
    need = State()


cancel_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❌ Отмена")],
    ],
    resize_keyboard=True
)


@router.message(StateFilter(TriggerStates.situation, TriggerStates.thought, TriggerStates.emotion, TriggerStates.body_reaction, TriggerStates.impulse, TriggerStates.need), Command("cancel"))
@router.message(StateFilter(TriggerStates.situation, TriggerStates.thought, TriggerStates.emotion, TriggerStates.body_reaction, TriggerStates.impulse, TriggerStates.need), F.text == "❌ Отмена")
async def cancel_trigger(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Ок, я отменил текущий сценарий.",
        reply_markup=main_menu
    )


@router.message(Command("trigger"))
@router.message(F.text == "🧠 Разобрать триггер")
async def start_trigger(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "Давай разберём триггер мягко и без самокритики.\n\n"
        "Важно: мы не будем глубоко погружаться в травму. "
        "Сначала просто посмотрим на цепочку: событие → мысль → эмоция → реакция.\n\n"
        "Первый вопрос:\n\n"
        "Что произошло прямо перед тем, как тебя накрыло?\n\n"
        "Например: «человек не ответил», «начальник сделал замечание», «мама сказала неприятную фразу».",
        reply_markup=cancel_menu
    )

    await state.set_state(TriggerStates.situation)


@router.message(TriggerStates.situation)
async def trigger_situation(message: Message, state: FSMContext):
    situation = (message.text or "").strip()

    if not situation:
        await message.answer("Напиши, пожалуйста, хотя бы пару слов о ситуации.")
        return

    await state.update_data(situation=situation)

    await message.answer(
        "Спасибо.\n\n"
        "Теперь вопрос 2:\n\n"
        "Какая мысль возникла в этот момент?\n\n"
        "Например:\n"
        "— «я ему/ей не важен/не важна»\n"
        "— «я всё испортил/испортила»\n"
        "— «меня сейчас отвергнут»\n"
        "— «со мной что-то не так»"
    )

    await state.set_state(TriggerStates.thought)


@router.message(TriggerStates.thought)
async def trigger_thought(message: Message, state: FSMContext):
    thought = (message.text or "").strip()

    if not thought:
        await message.answer("Напиши, пожалуйста, мысль, которая появилась в тот момент.")
        return

    await state.update_data(thought=thought)

    await message.answer(
        "Понял.\n\n"
        "Вопрос 3:\n\n"
        "Какая эмоция появилась сильнее всего?\n\n"
        "Например: тревога, злость, стыд, вина, обида, страх, одиночество, грусть."
    )

    await state.set_state(TriggerStates.emotion)


@router.message(TriggerStates.emotion)
async def trigger_emotion(message: Message, state: FSMContext):
    emotion = (message.text or "").strip()

    if not emotion:
        await message.answer("Напиши, пожалуйста, какую эмоцию ты заметил/заметила.")
        return

    await state.update_data(emotion=emotion)

    await message.answer(
        "Хорошо.\n\n"
        "Вопрос 4:\n\n"
        "Где это ощущалось в теле?\n\n"
        "Например:\n"
        "— сжало грудь;\n"
        "— ком в горле;\n"
        "— напряжение в животе;\n"
        "— тяжесть в плечах;\n"
        "— дрожь;\n"
        "— пустота."
    )

    await state.set_state(TriggerStates.body_reaction)


@router.message(TriggerStates.body_reaction)
async def trigger_body(message: Message, state: FSMContext):
    body_reaction = (message.text or "").strip()

    if not body_reaction:
        await message.answer("Напиши, пожалуйста, что происходило в теле.")
        return

    await state.update_data(body_reaction=body_reaction)

    await message.answer(
        "Спасибо.\n\n"
        "Вопрос 5:\n\n"
        "Чего тебе хотелось сделать на эмоциях?\n\n"
        "Например:\n"
        "— написать много сообщений;\n"
        "— замолчать;\n"
        "— убежать;\n"
        "— доказать;\n"
        "— накричать;\n"
        "— всё бросить;\n"
        "— спрятаться."
    )

    await state.set_state(TriggerStates.impulse)


@router.message(TriggerStates.impulse)
async def trigger_impulse(message: Message, state: FSMContext):
    impulse = (message.text or "").strip()

    if not impulse:
        await message.answer("Напиши, пожалуйста, какой импульс появился.")
        return

    await state.update_data(impulse=impulse)

    await message.answer(
        "Остался последний вопрос.\n\n"
        "Вопрос 6:\n\n"
        "Какая потребность могла быть задета?\n\n"
        "Например:\n"
        "— в безопасности;\n"
        "— в уважении;\n"
        "— в ясности;\n"
        "— в близости;\n"
        "— в принятии;\n"
        "— в отдыхе;\n"
        "— в праве быть услышанным/услышанной."
    )

    await state.set_state(TriggerStates.need)


@router.message(TriggerStates.need)
async def trigger_need(message: Message, state: FSMContext):
    need = (message.text or "").strip()

    if not need:
        await message.answer("Напиши, пожалуйста, какая потребность могла быть задета.")
        return

    await state.update_data(need=need)

    data = await state.get_data()

    telegram_id = message.from_user.id if message.from_user else 0

    save_trigger_entry(
        telegram_id=telegram_id,
        situation=data.get("situation"),
        thought=data.get("thought"),
        emotion=data.get("emotion"),
        body_reaction=data.get("body_reaction"),
        impulse=data.get("impulse"),
        need=data.get("need"),
    )

    await state.clear()

    response = (
        "Готово. Я сохранил разбор триггера 🧠\n\n"
        "Вот цепочка, которую мы увидели:\n\n"
        f"Ситуация: {data.get('situation')}\n"
        f"Мысль: {data.get('thought')}\n"
        f"Эмоция: {data.get('emotion')}\n"
        f"Тело: {data.get('body_reaction')}\n"
        f"Импульс: {data.get('impulse')}\n"
        f"Потребность: {data.get('need')}\n\n"
        "Мягкий вывод:\n"
        "Похоже, тебя задела не только сама ситуация, а то значение, которое мозг ей придал. "
        "Это не значит, что с тобой что-то не так. Это сигнал, что была важная потребность.\n\n"
        "Что можно сделать сейчас:\n"
        "1. Сделать паузу 5–10 минут.\n"
        "2. Не действовать на пике эмоции.\n"
        "3. Спросить себя: «Какой самый бережный следующий шаг?»\n\n"
        "Если состояние всё ещё сильное, можно нажать 🆘 «Меня накрыло»."
    )

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


@router.message(Command("trigger_stats"))
async def trigger_stats_command(message: Message):
    if not message.from_user:
        await message.answer("Не смог определить пользователя.")
        return

    count = get_trigger_count(message.from_user.id)

    await message.answer(
        "Статистика триггеров:\n\n"
        f"Сохранённых разборов: {count}\n\n"
        "Позже мы добавим эти данные в 📊 Мою карту, чтобы видеть повторяющиеся ситуации, мысли и потребности.",
        reply_markup=main_menu
    )