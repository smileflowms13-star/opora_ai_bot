import logging

from openai import AsyncOpenAI

from config import AI_API_KEY, AI_BASE_URL, AI_MODEL
from typing import Optional

from prompts import SYSTEM_PROMPT


logger = logging.getLogger(__name__)


AI_ENABLED = bool(AI_API_KEY and AI_MODEL)

client = None

if AI_ENABLED:
    client = AsyncOpenAI(
        api_key=AI_API_KEY,
        base_url=AI_BASE_URL,
    )


def _prepare_history(history):
    """
    Очищает историю перед отправкой в AI.
    Оставляем только роли user/assistant и непустой текст.

    Важно:
    - тексты сообщений пользователей здесь не логируем;
    - в логах не должно быть содержимого диалога.
    """
    clean_messages = []

    if not history:
        return clean_messages

    for item in history:
        if not isinstance(item, dict):
            continue

        role = item.get("role")
        content = item.get("content")

        if role not in ("user", "assistant"):
            continue

        if not content:
            continue

        clean_messages.append(
            {
                "role": role,
                "content": str(content),
            }
        )

    return clean_messages


async def generate_ai_reply(user_text: str, history=None, user_focus: Optional[str] = None) -> str:
    """
    Основная функция ответа AI.

    user_text — текущее сообщение пользователя.
    history — последние сообщения из базы.

    Важно:
    - user_text не логируем;
    - историю диалога не логируем;
    - API-ключи не логируем.
    """
    if not AI_ENABLED or client is None:
        logger.warning(
            "AI replies are disabled: api_key_configured=%s, model_configured=%s, base_url_configured=%s",
            bool(AI_API_KEY),
            bool(AI_MODEL),
            bool(AI_BASE_URL),
        )

        return (
            "Сейчас AI-ответы временно недоступны. "
            "Но ты можешь воспользоваться разделами: 🆘 Меня накрыло, 📝 Дневник, "
            "🧠 Разобрать триггер или 🌿 Упражнения."
        )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    # Если пользователь указал фокус внимания, добавляем уточняющую инструкцию
    if user_focus:
        messages.append(
            {
                "role": "system",
                "content": f"Пользователь сообщил, что его основной запрос: {user_focus}. Учитывай это в ответах, адаптируй упражнения и стиль поддержки под этот запрос.",
            }
        )

    clean_history = _prepare_history(history)

    if clean_history:
        messages.extend(clean_history)

    # Защита от дубля: если текущее сообщение уже есть последним в истории,
    # второй раз его не добавляем.
    if (
        not clean_history
        or clean_history[-1]["role"] != "user"
        or clean_history[-1]["content"] != user_text
    ):
        messages.append(
            {
                "role": "user",
                "content": user_text,
            }
        )

    try:
        response = await client.chat.completions.create(
            model=AI_MODEL,
            messages=messages,
            temperature=0.5,
            max_tokens=900,
        )

        if not response.choices:
            raise RuntimeError("AI returned response without choices")

        answer = response.choices[0].message.content

        if not answer:
            raise RuntimeError("AI returned empty answer")

        return answer.strip()

    except Exception as error:
        raise RuntimeError("AI provider request failed") from error


# Алиасы на случай, если где-то в проекте старая функция называлась иначе.
async def get_ai_response(user_text: str, history=None) -> str:
    return await generate_ai_reply(user_text, history=history)


async def ask_ai(user_text: str, history=None) -> str:
    return await generate_ai_reply(user_text, history=history)


async def get_ai_answer(user_text: str, history=None) -> str:
    return await generate_ai_reply(user_text, history=history)