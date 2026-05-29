import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ChatAction
from ai_client import generate_ai_reply
from database import get_diary_entries
from datetime import date, timedelta
from services.i18n import get_text
from keyboards import get_main_menu

router = Router()

SYSTEM_PROMPT = """Ты — бережный AI-аналитик дневника. Пользователь прислал свои записи дневника за последние 7 дней. 
Твоя задача — написать краткое (3-5 предложений) персонализированное резюме, основанное только на этих данных. 
Отметь основные паттерны (например, связь сна и настроения, повторяющиеся тревоги, улучшения). 
Дай одну мягкую рекомендацию или предложи подходящее упражнение из списка: 
«Дыхание 4–6», «5–4–3–2–1», «STOP», «Зона контроля», «Самосострадание», «Письмо без отправки», «Дыхание по квадрату».
Не используй слово "паттерн", будь простым и человечным. Не упоминай, что ты AI. 
Если данных недостаточно, скажи, что нужно больше записей для анализа."""

def _safe_get(row, key, default=""):
    try:
        return row[key] if key in row.keys() else default
    except:
        return default

def _format_diary_for_ai(entries) -> str:
    if not entries:
        return "Нет записей за последние 7 дней."
    lines = []
    for row in entries:
        date_str = _safe_get(row, "created_at")
        mood = _safe_get(row, "mood") or _safe_get(row, "mood_score")
        anxiety = _safe_get(row, "anxiety") or _safe_get(row, "anxiety_score")
        energy = _safe_get(row, "energy") or _safe_get(row, "energy_score")
        sleep = _safe_get(row, "sleep_quality") or _safe_get(row, "sleep")
        note = _safe_get(row, "note")
        lines.append(f"{date_str}: настроение {mood}/10, тревога {anxiety}/10, энергия {energy}/10, сон: {sleep}, заметка: {note}")
    return "\n".join(lines)

@router.message(Command("ai_insight"))
async def ai_insight_command(message: Message, **kwargs):
    if not message.from_user:
        await message.answer("Не смог определить пользователя.")
        return
    lang = kwargs.get("lang", "ru")
    telegram_id = message.from_user.id
    diary_entries = get_diary_entries(telegram_id)
    if not diary_entries:
        await message.answer(get_text("ai_insight_no_data", lang), reply_markup=get_main_menu(lang))
        return
    week_ago = date.today() - timedelta(days=7)
    recent = []
    for row in diary_entries:
        created_str = _safe_get(row, "created_at")
        if created_str:
            try:
                created_date = date.fromisoformat(created_str[:10])
                if created_date >= week_ago:
                    recent.append(row)
            except:
                continue
    if not recent:
        await message.answer(get_text("ai_insight_no_recent", lang), reply_markup=get_main_menu(lang))
        return
    user_text = _format_diary_for_ai(recent)
    try:
        await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
        ai_answer = await generate_ai_reply(user_text=user_text, history=[{"role": "system", "content": SYSTEM_PROMPT}], user_focus=None)
        ai_answer = (ai_answer or "").strip()
        if not ai_answer:
            ai_answer = get_text("ai_insight_empty", lang)
    except Exception as e:
        logging.exception("AI insight failed")
        ai_answer = get_text("ai_insight_error", lang)
    prefix = get_text("ai_insight_prefix", lang)
    await message.answer(f"{prefix}\n\n{ai_answer}", reply_markup=get_main_menu(lang))