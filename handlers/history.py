from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database import get_recent_messages
from services.i18n import get_text

router = Router()
PAGE_SIZE = 5

@router.message(Command("history"))
async def history_command(message: Message, state: FSMContext, **kwargs):
    if not message.from_user:
        await message.answer("User not identified.")
        return
    lang = kwargs.get("lang", "ru")
    telegram_id = message.from_user.id
    messages = get_recent_messages(telegram_id=telegram_id, limit=100, exclude_high_risk=False)
    if not messages:
        await message.answer(get_text("history_empty", lang))
        return
    await state.update_data(history_messages=messages, history_page=0)
    await _show_page(message, messages, 0, lang)

async def _show_page(message, messages: list, page: int, lang: str):
    total_pages = (len(messages) + PAGE_SIZE - 1) // PAGE_SIZE
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    chunk = messages[start:end]
    lines = []
    for msg in chunk:
        role = "🤖" if msg["role"] == "assistant" else "👤"
        text = msg["content"][:100].replace("\n", " ")
        lines.append(f"{role} {text}")
    text = f"{get_text('history_title', lang)} {page + 1}/{total_pages}\n\n" + "\n\n".join(lines)
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton(text="◀️ Назад", callback_data="hist_prev"))
    if page < total_pages - 1:
        buttons.append(InlineKeyboardButton(text="Вперёд ▶️", callback_data="hist_next"))
    kb = InlineKeyboardMarkup(inline_keyboard=[buttons]) if buttons else None
    await message.answer(text, reply_markup=kb)

@router.callback_query(F.data.in_({"hist_prev", "hist_next"}))
async def history_page(callback: CallbackQuery, state: FSMContext, **kwargs):
    data = await state.get_data()
    messages = data.get("history_messages", [])
    page = data.get("history_page", 0)
    lang = kwargs.get("lang", "ru")
    if callback.data == "hist_prev":
        page -= 1
    elif callback.data == "hist_next":
        page += 1
    page = max(0, min(page, (len(messages) - 1) // PAGE_SIZE))
    await state.update_data(history_page=page)
    await _show_page(callback.message, messages, page, lang)
    await callback.answer()