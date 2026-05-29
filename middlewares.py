from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from database import user_has_consent, get_user_language
from keyboards import get_onboarding_menu
from safety import is_high_risk
from services.i18n import get_text

class LanguageMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = None
        if isinstance(event, Message):
            user = event.from_user
        elif isinstance(event, CallbackQuery):
            user = event.from_user
        if user:
            db_lang = get_user_language(user.id)
            if db_lang:
                lang = db_lang
            else:
                lang = user.language_code if user.language_code in ("ru", "en", "hi", "zh") else "ru"
        else:
            lang = "ru"
        data["lang"] = lang
        return await handler(event, data)

class ConsentMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if not isinstance(event, Message):
            return await handler(event, data)
        user = event.from_user
        if user is None:
            return await handler(event, data)
        text = (event.text or event.caption or "").strip()
        lang = data.get("lang", "ru")
        if text and is_high_risk(text):
            await event.answer(get_text("crisis_text", lang))
            return None
        if text.startswith("/start"):
            return await handler(event, data)
        if text in [get_text("consent_accept_button", "ru"), get_text("consent_accept_button", "en"),
                    get_text("consent_decline_button", "ru"), get_text("consent_decline_button", "en")]:
            return await handler(event, data)
        if user_has_consent(user.id):
            return await handler(event, data)
        await event.answer(get_text("onboarding_text", lang), reply_markup=get_onboarding_menu(lang))
        return None