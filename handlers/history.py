from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from database import get_recent_messages
from keyboards import main_menu
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

MESSAGES_PER_PAGE = 5
MAX_HISTORY_MESSAGES = 30

class HistoryStates(StatesGroup):
    viewing = State()

def format_message(role, content, index):
    prefix = "Вы" if role == "user" else "Опора AI"
    return f"{prefix}: {content}\n\n"

def build_page(messages, offset):
    page_messages = messages[offset:offset + MESSAGES_PER_PAGE]
    text = f"📜 История диалогов ({offset + 1}–{min(offset + MESSAGES_PER_PAGE, len(messages))} из {len(messages)}):\n\n"
    for i, msg in enumerate(page_messages):
        text += f"{offset + i + 1}. {format_message(msg['role'], msg['content'], offset + i)}"
    return text

def pagination_keyboard(offset, total):
    buttons = []
    if offset > 0:
        buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"history_page_{offset - MESSAGES_PER_PAGE}"))
    if offset + MESSAGES_PER_PAGE < total:
        buttons.append(InlineKeyboardButton(text="Вперёд ➡️", callback_data=f"history_page_{offset + MESSAGES_PER_PAGE}"))
    buttons.append(InlineKeyboardButton(text="❌ Закрыть", callback_data="history_close"))
    return InlineKeyboardMarkup(inline_keyboard=[buttons])

@router.message(Command("history"))
async def history_command(message: Message):
    if not message.from_user:
        await message.answer("Не смог определить пользователя.")
        return
    telegram_id = message.from_user.id
    messages = get_recent_messages(telegram_id=telegram_id, limit=MAX_HISTORY_MESSAGES)
    if not messages:
        await message.answer("Пока нет истории диалогов.", reply_markup=main_menu)
        return
    # Сохраним сообщения в состояние, чтобы избежать повторных запросов
    # Но проще передавать в callback_data offset, а сообщения хранить в состоянии
    # Используем состояние
    from aiogram.fsm.context import FSMContext
    state: FSMContext = FSMContext(storage=MemoryStorage(), key=message.chat.id)
    await state.set_state(HistoryStates.viewing)
    await state.update_data(messages=messages)
    text = build_page(messages, 0)
    await message.answer(text, reply_markup=pagination_keyboard(0, len(messages)))

@router.callback_query(F.data.startswith("history_page_"))
async def history_page_callback(callback: CallbackQuery, state: FSMContext):
    offset = int(callback.data.split("_")[-1])
    data = await state.get_data()
    messages = data.get("messages", [])
    if not messages:
        await callback.answer("История больше не доступна.")
        return
    text = build_page(messages, offset)
    await callback.message.edit_text(text, reply_markup=pagination_keyboard(offset, len(messages)))
    await callback.answer()

@router.callback_query(F.data == "history_close")
async def history_close(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.answer("История закрыта.")