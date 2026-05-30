import pytest
from unittest.mock import AsyncMock, patch
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, Chat, User, CallbackQuery

from handlers.history import history_command, history_page
from services.i18n import get_text


@pytest.fixture
def message():
    msg = AsyncMock(spec=Message)
    msg.from_user = User(id=12345, is_bot=False, first_name="Test")
    msg.chat = Chat(id=12345, type="private")
    msg.answer = AsyncMock()
    return msg


@pytest.fixture
def state():
    return AsyncMock(spec=FSMContext)


@pytest.mark.asyncio
async def test_history_empty(message, state):
    with patch('handlers.history.get_recent_messages', return_value=[]):
        await history_command(message, state, lang='ru')
        message.answer.assert_called_once_with(get_text("history_empty", "ru"))


@pytest.mark.asyncio
async def test_history_with_data(message, state):
    messages = [
        {"role": "user", "content": "Привет"},
        {"role": "assistant", "content": "Здравствуйте!"},
        {"role": "user", "content": "Как справиться с тревогой?"},
        {"role": "assistant", "content": "Попробуйте дыхательные упражнения"},
        {"role": "user", "content": "Спасибо"},
        {"role": "assistant", "content": "Пожалуйста"},
    ]
    with patch('handlers.history.get_recent_messages', return_value=messages):
        await history_command(message, state, lang='ru')
        state.update_data.assert_called_with(history_messages=messages, history_page=0)
        text = message.answer.call_args[0][0]
        assert "1/2" in text
        assert "Привет" in text

        # Кнопка "Вперёд"
        cb = AsyncMock(spec=CallbackQuery)
        cb.data = "hist_next"
        cb.message = message
        cb.answer = AsyncMock()
        state.get_data.return_value = {"history_messages": messages, "history_page": 0}
        await history_page(cb, state, lang='ru')
        text2 = message.answer.call_args[0][0]
        assert "2/2" in text2
        assert "Пожалуйста" in text2

        # Кнопка "Назад"
        cb.data = "hist_prev"
        state.get_data.return_value = {"history_messages": messages, "history_page": 1}
        await history_page(cb, state, lang='ru')
        text3 = message.answer.call_args[0][0]
        assert "1/2" in text3