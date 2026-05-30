import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message, Chat, User

from handlers.map import map_command
from services.i18n import get_text


@pytest.fixture
def message():
    msg = AsyncMock(spec=Message)
    msg.from_user = User(id=12345, is_bot=False, first_name="Test")
    msg.chat = Chat(id=12345, type="private")
    msg.text = get_text("map_button_text", "ru")
    msg.answer = AsyncMock()
    return msg


@pytest.mark.asyncio
async def test_map_returns_data(message):
    with patch('handlers.map.build_user_map', return_value="📊 Моя карта\n\n...") as mock_build:
        await map_command(message, lang='ru')
        mock_build.assert_called_once_with(12345)
        message.answer.assert_called_once()
        assert "📊 Моя карта" in message.answer.call_args[0][0]


@pytest.mark.asyncio
async def test_map_no_user(message):
    message.from_user = None
    await map_command(message, lang='ru')
    message.answer.assert_called_once()
    assert "Не смог определить" in message.answer.call_args[0][0]