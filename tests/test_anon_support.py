import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, Chat, User, ReplyKeyboardMarkup

from handlers.support import (
    start_support, handle_support_message, handle_support_reply,
    SupportStates, get_anonymous_id, get_or_create_topic, get_support_close_menu
)
from config import SUPPORT_GROUP_ID
from services.i18n import get_text
from database import get_connection


@pytest.fixture
def message():
    msg = AsyncMock(spec=Message)
    msg.from_user = User(id=12345, is_bot=False, first_name="Test")
    msg.chat = Chat(id=12345, type="private")
    msg.text = ""
    msg.answer = AsyncMock()
    return msg


@pytest.fixture
def state():
    return AsyncMock(spec=FSMContext)


@pytest.mark.asyncio
async def test_start_support(message, state):
    await start_support(message, state, lang='ru')
    message.answer.assert_called_once()
    args, kwargs = message.answer.call_args
    assert get_text("anon_support_intro", "ru") in args[0]
    state.set_state.assert_called_with(SupportStates.waiting_for_message)


@pytest.mark.asyncio
async def test_send_anon_message_creates_topic(message, state):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    mock_bot = AsyncMock()
    mock_bot.create_forum_topic = AsyncMock(return_value=MagicMock(message_thread_id=100))
    mock_bot.send_message = AsyncMock()

    with patch('handlers.support.get_connection', return_value=mock_conn), \
         patch('handlers.support._now', return_value='2025-05-31T12:00:00'):
        
        message.text = "Привет, мне нужна помощь"
        await handle_support_message(message, state, bot=mock_bot, lang='ru')

        mock_bot.create_forum_topic.assert_called_once_with(
            chat_id=SUPPORT_GROUP_ID,
            name=f"Аноним #{get_anonymous_id(12345)}"
        )
        mock_bot.send_message.assert_called_once()
        call_kwargs = mock_bot.send_message.call_args[1]
        assert call_kwargs['chat_id'] == SUPPORT_GROUP_ID
        assert call_kwargs.get('message_thread_id') == 100
        message.answer.assert_called_with(get_text("anon_support_sent", "ru"))


@pytest.mark.asyncio
async def test_close_request(message, state):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {"topic_id": 200}

    mock_bot = AsyncMock()
    mock_bot.send_message = AsyncMock()

    with patch('handlers.support.get_connection', return_value=mock_conn):
        message.text = get_text("close_request_button", "ru")
        await handle_support_message(message, state, bot=mock_bot, lang='ru')

        mock_cursor.execute.assert_any_call(
            "DELETE FROM anon_support WHERE anon_id = ?",
            (get_anonymous_id(12345),)
        )
        mock_bot.send_message.assert_called_with(
            SUPPORT_GROUP_ID,
            f"🔒 Пользователь закрыл обращение (Аноним #{get_anonymous_id(12345)}).",
            message_thread_id=200
        )
        state.clear.assert_called()
        message.answer.assert_called()


@pytest.mark.asyncio
async def test_support_reply():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (12345,)

    reply_msg = AsyncMock(spec=Message)
    reply_msg.from_user = User(id=999, is_bot=False, first_name="Volunteer")
    reply_msg.chat = Chat(id=SUPPORT_GROUP_ID, type="supergroup")
    reply_msg.message_thread_id = 300
    reply_msg.text = "Держитесь, всё будет хорошо"

    mock_bot = AsyncMock()
    mock_bot.send_message = AsyncMock()

    with patch('handlers.support.get_connection', return_value=mock_conn), \
         patch('database.get_user_language', return_value='ru'):   # <-- исправлено
        await handle_support_reply(reply_msg, bot=mock_bot)

        mock_bot.send_message.assert_called_once()
        call_args = mock_bot.send_message.call_args[0]
        assert call_args[0] == 12345
        assert "Держитесь, всё будет хорошо" in call_args[1]