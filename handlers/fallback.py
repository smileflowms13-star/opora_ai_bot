import logging

from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.types import Message

from ai_client import generate_ai_reply
from database import add_user, save_message, get_recent_messages
from safety import is_high_risk
from texts import CRISIS_TEXT


router = Router()
logger = logging.getLogger(__name__)


AI_TEMPORARY_ERROR_TEXT = (
    "Похоже, сейчас не получилось получить ответ от AI-сервиса.\n\n"
    "Попробуй, пожалуйста, ещё раз чуть позже. "
    "А если тебя прямо сейчас накрыло — можно выбрать кнопку «🆘 Меня накрыло» "
    "и сделать короткое упражнение для стабилизации."
)


@router.message()
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
    # Даже если middleware по какой-то причине не перехватил high-risk,
    # fallback не должен отправлять такое сообщение в AI
    # и не должен сохранять его в обычную AI-историю.
    if is_high_risk(user_text):
        await message.answer(CRISIS_TEXT)
        return

    # Команды не отправляем в AI.
    # Например, если пользователь ошибся в команде: /triger вместо /trigger.
    if user_text.startswith("/"):
        await message.answer(
            "Я не нашёл такую команду.\n\n"
            "Попробуй открыть меню командой /menu или выбрать действие кнопками."
        )
        return

    # Сохраняем только обычное сообщение пользователя.
    # ВАЖНО: не передаём risk_level, потому что текущая save_message()
    # в database.py его не принимает.
    save_message(
        telegram_id=telegram_id,
        role="user",
        content=user_text,
    )

    try:
        # Берём последние сообщения из базы.
        # Они уже включают текущее сообщение пользователя.
        history = get_recent_messages(
            telegram_id=telegram_id,
            limit=12,
        )

        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.TYPING,
        )

        ai_answer = await generate_ai_reply(
            user_text=user_text,
            history=history,
        )

        ai_answer = (ai_answer or "").strip()

        if not ai_answer:
            raise RuntimeError("AI returned empty answer")

    except Exception:
        logger.exception("AI reply generation failed for telegram_id=%s", telegram_id)

        await message.answer(AI_TEMPORARY_ERROR_TEXT)
        return

    save_message(
        telegram_id=telegram_id,
        role="assistant",
        content=ai_answer,
    )

    await message.answer(ai_answer)