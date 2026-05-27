import logging

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.enums import ChatAction
from aiogram.types import Message

from ai_client import generate_ai_reply
from database import add_user, save_message, get_recent_messages, get_user_focus, get_crisis_plan
from safety import is_high_risk, sanitize_user_input
from texts import CRISIS_TEXT


logger = logging.getLogger(__name__)

router = Router()


MAX_USER_TEXT_LENGTH = 3000


AI_TEMPORARY_ERROR_TEXT = (
    "Похоже, сейчас не получилось получить ответ от AI-сервиса.\n\n"
    "Попробуй, пожалуйста, ещё раз чуть позже. "
    "А если тебя прямо сейчас накрыло — можно выбрать кнопку «🆘 Меня накрыло» "
    "и сделать короткое упражнение для стабилизации."
)


TOO_LONG_MESSAGE_TEXT = (
    "Сообщение получилось очень длинным.\n\n"
    "Я смогу лучше помочь, если ты сократишь его до нескольких абзацев: "
    "что случилось, что ты чувствуешь и какая помощь сейчас нужна."
)


@router.message(StateFilter(None))
async def fallback_message(message: Message):
    user = message.from_user

    if user:
        add_user(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
        )

    telegram_id = user.id if user else message.chat.id

    user_text = message.text or message.caption or ""
    user_text = user_text.strip()

    if not user_text:
        await message.answer(
            "Я лучше понимаю текстовые сообщения. Напиши, пожалуйста, словами, что сейчас происходит."
        )
        return

    # Safety first.
    if is_high_risk(user_text):
        await message.answer(CRISIS_TEXT)
        # Показываем кризисный план, если он есть
        if user:
            plan = get_crisis_plan(user.id)
            if plan:
                await message.answer(f"Твой кризисный план:\n\n{plan}")
        return

    # Команды не отправляем в AI.
    if user_text.startswith("/"):
        await message.answer(
            "Я не нашёл такую команду.\n\n"
            "Попробуй открыть меню командой /menu или выбрать действие кнопками."
        )
        return

    # Слишком длинные сообщения не сохраняем и не отправляем в AI.
    if len(user_text) > MAX_USER_TEXT_LENGTH:
        await message.answer(TOO_LONG_MESSAGE_TEXT)
        return

    # --- Защита от инъекций: очищаем ввод перед отправкой в AI ---
    user_text_clean = sanitize_user_input(user_text)
    # -------------------------------------------------------------

    save_message(
        telegram_id=telegram_id,
        role="user",
        content=user_text_clean,
    )

    try:
        history = get_recent_messages(
            telegram_id=telegram_id,
            limit=12,
        )

        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.TYPING,
        )

        user_focus = get_user_focus(telegram_id)

        ai_answer = await generate_ai_reply(
            user_text=user_text_clean,
            history=history,
            user_focus=user_focus,
        )

        ai_answer = (ai_answer or "").strip()

        if not ai_answer:
            raise RuntimeError("AI returned empty answer")

    except Exception:
        logger.exception(
            "AI request failed for telegram_id=%s",
            message.from_user.id if message.from_user else None,
        )
        await message.answer(AI_TEMPORARY_ERROR_TEXT)
        return

    save_message(
        telegram_id=telegram_id,
        role="assistant",
        content=ai_answer,
    )

    await message.answer(ai_answer)