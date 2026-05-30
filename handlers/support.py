import hashlib
import logging
import sys
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode

from config import SUPPORT_GROUP_ID
from database import get_connection, _now
from keyboards import get_main_menu
from services.i18n import get_text

router = Router()

class SupportStates(StatesGroup):
    waiting_for_message = State()

def get_anonymous_id(telegram_id: int) -> str:
    salt = "opora_support_2025"
    hash_input = f"{telegram_id}{salt}".encode()
    return hashlib.sha256(hash_input).hexdigest()[:8]

def get_support_close_menu(lang: str) -> ReplyKeyboardMarkup:
    """Клавиатура с кнопкой 'Завершить обращение'."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=get_text("close_request_button", lang))]],
        resize_keyboard=True
    )

async def get_or_create_topic(bot: Bot, anon_id: str) -> int | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT topic_id FROM anon_support WHERE anon_id = ?", (anon_id,))
    row = cursor.fetchone()
    if row and row["topic_id"]:
        topic_id = row["topic_id"]
        conn.close()
        return topic_id

    try:
        topic = await bot.create_forum_topic(
            chat_id=SUPPORT_GROUP_ID,
            name=f"Аноним #{anon_id}",
        )
        topic_id = topic.message_thread_id
        cursor.execute(
            "UPDATE anon_support SET topic_id = ? WHERE anon_id = ?",
            (topic_id, anon_id),
        )
        conn.commit()
        print(f"DEBUG: Topic created for {anon_id}, topic_id={topic_id}")
        sys.stdout.flush()
        return topic_id
    except Exception as e:
        print(f"DEBUG: Could not create topic for {anon_id}: {e}")
        sys.stdout.flush()
        return None
    finally:
        conn.close()

@router.message(Command("support"))
@router.message(F.text.in_([get_text("anon_support_button", "ru"), get_text("anon_support_button", "en")]))
async def start_support(message: Message, state: FSMContext, **kwargs):
    lang = kwargs.get("lang", "ru")
    await message.answer(
        get_text("anon_support_intro", lang),
        reply_markup=get_support_close_menu(lang),
        parse_mode=ParseMode.HTML
    )
    await state.set_state(SupportStates.waiting_for_message)

@router.message(SupportStates.waiting_for_message)
async def handle_support_message(message: Message, state: FSMContext, bot: Bot, **kwargs):
    lang = kwargs.get("lang", "ru")
    user_text = message.text.strip() if message.text else ""

    # Проверяем, не нажата ли кнопка "Завершить обращение"
    if user_text == get_text("close_request_button", lang):
        telegram_id = message.from_user.id
        anon_id = get_anonymous_id(telegram_id)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT topic_id FROM anon_support WHERE anon_id = ?", (anon_id,))
        row = cursor.fetchone()
        topic_id = row["topic_id"] if row else None

        cursor.execute("DELETE FROM anon_support WHERE anon_id = ?", (anon_id,))
        conn.commit()
        conn.close()

        if topic_id:
            try:
                await bot.send_message(
                    SUPPORT_GROUP_ID,
                    f"🔒 Пользователь закрыл обращение (Аноним #{anon_id}).",
                    message_thread_id=topic_id
                )
            except Exception as e:
                print(f"ERROR notifying support group about closed request: {e}")

        await state.clear()
        await message.answer(get_text("request_closed", lang), reply_markup=get_main_menu(lang))
        return

    # Иначе пересылаем сообщение в группу поддержки
    if not user_text:
        await message.answer(get_text("diary_note_empty", lang))
        return

    user_telegram_id = message.from_user.id
    anon_id = get_anonymous_id(user_telegram_id)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO anon_support (anon_id, telegram_id, created_at)
        VALUES (?, ?, ?)
        ON CONFLICT(anon_id) DO UPDATE SET telegram_id = excluded.telegram_id
        """,
        (anon_id, user_telegram_id, _now()),
    )
    conn.commit()
    conn.close()

    topic_id = await get_or_create_topic(bot, anon_id)

    group_message = (
        f"🆔 <b>Аноним #{anon_id}</b>\n"
        f"📩 Сообщение:\n"
        f"{user_text}"
    )

    try:
        kwargs_send = {"chat_id": SUPPORT_GROUP_ID, "text": group_message, "parse_mode": ParseMode.HTML}
        if topic_id:
            kwargs_send["message_thread_id"] = topic_id
        await bot.send_message(**kwargs_send)
        print(f"DEBUG: Message sent to support group, topic_id={topic_id}")
        sys.stdout.flush()
    except Exception as e:
        error_msg = str(e)
        print(f"ERROR sending to support group: {error_msg}")
        sys.stdout.flush()
        if "message thread not found" in error_msg and topic_id:
            print("DEBUG: Removing invalid topic_id and retrying without thread")
            conn = get_connection()
            conn.execute("UPDATE anon_support SET topic_id = NULL WHERE anon_id = ?", (anon_id,))
            conn.commit()
            conn.close()
            try:
                await bot.send_message(SUPPORT_GROUP_ID, group_message, parse_mode=ParseMode.HTML)
                print("DEBUG: Message sent to support group (fallback to general chat)")
            except Exception as e2:
                print(f"ERROR: Fallback also failed: {e2}")
                await message.answer(
                    get_text("anon_support_error", lang),
                    reply_markup=get_main_menu(lang)
                )
                await state.clear()
                return
        else:
            await message.answer(
                get_text("anon_support_error", lang),
                reply_markup=get_main_menu(lang)
            )
            await state.clear()
            return

    # Подтверждение пользователю
    await message.answer(get_text("anon_support_sent", lang))

# === Обработчик ответов поддержки (автоматически по теме) ===
@router.message(F.chat.id == SUPPORT_GROUP_ID)
async def handle_support_reply(message: Message, bot: Bot):
    if message.from_user and message.from_user.is_bot:
        return

    topic_id = message.message_thread_id
    if not topic_id:
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT telegram_id FROM anon_support WHERE topic_id = ?",
        (topic_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return

    target_telegram_id = row[0]
    reply_text = message.text or message.caption or ""
    if not reply_text:
        return

    try:
        from database import get_user_language
        user_lang = get_user_language(target_telegram_id) or "ru"
        reply_message = get_text("anon_support_reply", user_lang).format(reply_text=reply_text)
        await bot.send_message(
            target_telegram_id,
            reply_message,
            parse_mode=ParseMode.HTML,
        )
        print(f"DEBUG: Reply sent to user {target_telegram_id}")
        sys.stdout.flush()
    except Exception as e:
        print(f"ERROR sending reply to user {target_telegram_id}: {e}")