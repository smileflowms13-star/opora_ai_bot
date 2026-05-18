from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from database import user_has_consent
from keyboards import onboarding_menu
from safety import is_high_risk
from texts import (
    CONSENT_ACCEPT_BUTTON,
    CONSENT_DECLINE_BUTTON,
    CRISIS_TEXT,
    ONBOARDING_TEXT,
)


class ConsentMiddleware(BaseMiddleware):
    """
    Middleware допускает к обычным разделам только пользователей,
    которые подтвердили 18+ и приняли правила.

    Исключения:
    - /start;
    - кнопки принятия/отказа;
    - high-risk сообщения: сразу кризисный протокол.
    """

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        user = event.from_user
        if user is None:
            return await handler(event, data)

        text = (event.text or event.caption or "").strip()

        # 1. Safety first: рискованные сообщения не блокируем онбордингом,
        # а сразу отдаём кризисный протокол.
        if text and is_high_risk(text):
            await event.answer(CRISIS_TEXT)
            return None

        # 2. /start всегда разрешён.
        if text.startswith("/start"):
            return await handler(event, data)

        # 3. Кнопки онбординга всегда разрешены.
        if text in {CONSENT_ACCEPT_BUTTON, CONSENT_DECLINE_BUTTON}:
            return await handler(event, data)

        # 4. Если согласие уже есть — пропускаем дальше.
        if user_has_consent(user.id):
            return await handler(event, data)

        # 5. Иначе показываем онбординг.
        await event.answer(
            ONBOARDING_TEXT,
            reply_markup=onboarding_menu,
        )
        return None