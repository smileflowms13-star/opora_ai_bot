import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, Chat, User

from handlers.exercises import (
    start_breathing, BreathingSteps,
    exit_breathing,
    grounding_finish_exit, exit_grounding,
    start_grounding,
    listen_step,
    next_step
)
from services.i18n import get_text
from services.streak_service import process_streak


@pytest.fixture
def fsm_context():
    ctx = AsyncMock(spec=FSMContext)
    ctx.get_state.return_value = None
    ctx.get_data.return_value = {}
    ctx.set_state = AsyncMock()
    ctx.update_data = AsyncMock()
    ctx.clear = AsyncMock()
    return ctx


@pytest.fixture
def message():
    msg = AsyncMock(spec=Message)
    msg.from_user = User(id=12345, is_bot=False, first_name="Test")
    msg.chat = Chat(id=12345, type="private")
    msg.text = ""
    msg.answer = AsyncMock()
    msg.edit_text = AsyncMock()
    return msg


@pytest.fixture
def callback():
    cb = AsyncMock(spec=CallbackQuery)
    cb.from_user = User(id=12345, is_bot=False, first_name="Test")
    cb.message = AsyncMock(spec=Message)
    cb.message.chat = Chat(id=12345, type="private")
    cb.message.text = "some text"
    cb.message.edit_text = AsyncMock()
    cb.message.answer = AsyncMock()
    cb.message.answer_audio = AsyncMock()
    cb.answer = AsyncMock()
    cb.data = ""
    return cb


@pytest.mark.asyncio
async def test_breathing_full_ru(message, fsm_context):
    with patch('handlers.exercises.process_streak', return_value=None):
        await start_breathing(message, fsm_context, lang='ru')
        message.answer.assert_called_once()
        args, kwargs = message.answer.call_args
        assert get_text("breathing_intro", "ru") in args[0]
        fsm_context.set_state.assert_called_with(BreathingSteps.intro)

        cb = AsyncMock(spec=CallbackQuery)
        cb.message = message
        cb.data = "breathing_next"
        cb.from_user = message.from_user
        cb.answer = AsyncMock()

        # Шаг inhale
        fsm_context.get_state.return_value = BreathingSteps.intro.state
        await next_step(cb, fsm_context, lang='ru')
        cb.message.edit_text.assert_called()
        assert get_text("breathing_step_inhale", "ru") in cb.message.edit_text.call_args[0][0]

        # hold_in
        fsm_context.get_state.return_value = BreathingSteps.inhale.state
        await next_step(cb, fsm_context, lang='ru')
        assert get_text("breathing_step_hold_in", "ru") in cb.message.edit_text.call_args[0][0]

        # exhale
        fsm_context.get_state.return_value = BreathingSteps.hold_in.state
        await next_step(cb, fsm_context, lang='ru')
        assert get_text("breathing_step_exhale", "ru") in cb.message.edit_text.call_args[0][0]

        # hold_out
        fsm_context.get_state.return_value = BreathingSteps.exhale.state
        await next_step(cb, fsm_context, lang='ru')
        assert get_text("breathing_step_hold_out", "ru") in cb.message.edit_text.call_args[0][0]

        # finish
        fsm_context.get_state.return_value = BreathingSteps.hold_out.state
        await next_step(cb, fsm_context, lang='ru')
        assert get_text("breathing_finish", "ru") in cb.message.edit_text.call_args[0][0]


@pytest.mark.asyncio
async def test_breathing_cancel_ru(message, fsm_context):
    with patch('handlers.exercises.process_streak', return_value=None):
        await start_breathing(message, fsm_context, lang='ru')
        cb = AsyncMock(spec=CallbackQuery)
        cb.message = message
        cb.data = "breathing_exit"
        cb.from_user = message.from_user
        cb.answer = AsyncMock()

        await exit_breathing(cb, fsm_context, lang='ru')
        fsm_context.clear.assert_called()
        cb.message.answer.assert_called()


@pytest.mark.asyncio
async def test_grounding_full_ru(message, fsm_context):
    with patch('handlers.exercises.process_streak', return_value="Стрик обновлён!") as mock_streak:
        await start_grounding(message, fsm_context, lang='ru')
        message.answer.assert_called()
        fsm_context.set_state.assert_called()

        cb = AsyncMock(spec=CallbackQuery)
        cb.message = message
        cb.data = "grounding_next"
        cb.from_user = message.from_user
        cb.answer = AsyncMock()

        fsm_context.get_state.return_value = "GroundingSteps:finish"
        cb.data = "grounding_exit"
        await grounding_finish_exit(cb, fsm_context, lang='ru')
        mock_streak.assert_called_once_with(12345)
        fsm_context.clear.assert_called()
        cb.message.answer.assert_called()


@pytest.mark.asyncio
async def test_exercise_cancel_grounding(message, fsm_context):
    with patch('handlers.exercises.process_streak', return_value=None):
        await start_grounding(message, fsm_context, lang='ru')
        cb = AsyncMock(spec=CallbackQuery)
        cb.message = message
        cb.data = "grounding_exit"
        cb.from_user = message.from_user
        cb.answer = AsyncMock()

        await exit_grounding(cb, fsm_context, lang='ru')
        fsm_context.clear.assert_called()
        cb.message.answer.assert_called()


@pytest.mark.asyncio
async def test_listen_step(message, fsm_context):
    cb = AsyncMock(spec=CallbackQuery)
    cb.message = message
    cb.data = "listen"
    cb.answer = AsyncMock()
    cb.bot = AsyncMock()
    cb.bot.send_chat_action = AsyncMock()
    cb.message.answer_audio = AsyncMock()

    fsm_context.get_data.return_value = {"current_text": "Привет, это тест."}

    with patch('handlers.exercises.gTTS') as mock_gtts:
        mock_tts = MagicMock()
        mock_tts.save = MagicMock()
        mock_gtts.return_value = mock_tts

        await listen_step(cb, fsm_context)
        cb.message.answer_audio.assert_called()
        mock_gtts.assert_called_once_with(text="Привет, это тест.", lang="ru")