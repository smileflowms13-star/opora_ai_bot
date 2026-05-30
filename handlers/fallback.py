import logging
from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.enums import ChatAction
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from ai_client import generate_ai_reply
from database import add_user, save_message, get_recent_messages, get_user_focus, get_crisis_plan
from safety import is_high_risk, sanitize_user_input
from services.analytics import get_quick_exercise_suggestions
from services.i18n import get_text
from config import SUPPORT_GROUP_ID

logger = logging.getLogger(__name__)
router = Router()
MAX_USER_TEXT_LENGTH = 3000

@router.message(StateFilter(None))
async def fallback_message(message: Message, **kwargs):
    # Игнорируем сообщения из группы поддержки
    if message.chat and message.chat.id == SUPPORT_GROUP_ID:
        return

    user = message.from_user
    lang = kwargs.get("lang", "ru")
    if user:
        add_user(telegram_id=user.id, username=user.username, first_name=user.first_name)
    telegram_id = user.id if user else message.chat.id
    user_text = message.text or message.caption or ""
    user_text = user_text.strip()

    if not user_text:
        await message.answer(get_text("fallback_not_text", lang))
        return
    if is_high_risk(user_text):
        await message.answer(get_text("crisis_text", lang))
        if user:
            plan = get_crisis_plan(user.id)
            if plan:
                await message.answer(f"{get_text('crisis_plan_prefix', lang)}\n\n{plan}")
        return
    suggestions = get_quick_exercise_suggestions(user_text)
    if suggestions:
        keyboard_rows = []
        for exercise in suggestions:
            keyboard_rows.append([InlineKeyboardButton(text=exercise, callback_data=f"quick_exercise_{exercise}")])
        await message.answer(get_text("fallback_quick_exercise", lang),
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_rows))
        return
    if user_text.startswith("/"):
        await message.answer(get_text("fallback_unknown_command", lang))
        return
    if len(user_text) > MAX_USER_TEXT_LENGTH:
        await message.answer(get_text("fallback_too_long", lang))
        return
    user_text_clean = sanitize_user_input(user_text)
    save_message(telegram_id=telegram_id, role="user", content=user_text_clean)
    try:
        history = get_recent_messages(telegram_id=telegram_id, limit=12)
        await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
        user_focus = get_user_focus(telegram_id)
        ai_answer = await generate_ai_reply(user_text=user_text_clean, history=history, user_focus=user_focus)
        ai_answer = (ai_answer or "").strip()
        if not ai_answer:
            raise RuntimeError("AI returned empty answer")
    except Exception:
        logger.exception("AI request failed")
        await message.answer(get_text("ai_error_text", lang))
        return
    save_message(telegram_id=telegram_id, role="assistant", content=ai_answer)
    await message.answer(ai_answer)