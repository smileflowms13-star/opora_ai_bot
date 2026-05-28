from typing import Optional
from database import update_streak, get_streak
from texts import (
    STREAK_UPDATED_TEXT,
    STREAK_LEVEL_UP_TO_FLOWER,
    STREAK_LEVEL_UP_TO_TREE,
)

def process_streak(telegram_id: int) -> Optional[str]:
    """
    Обновляет ежедневный стрик пользователя и возвращает сообщение для отправки.
    Возвращает None, если сообщение не требуется (например, стрик уже был обновлён сегодня).
    """
    update_streak(telegram_id)
    streak_data = get_streak(telegram_id)

    if streak_data["current_streak"] == 30:
        return STREAK_LEVEL_UP_TO_TREE
    elif streak_data["current_streak"] == 7:
        return STREAK_LEVEL_UP_TO_FLOWER
    else:
        return STREAK_UPDATED_TEXT.format(streak=streak_data["current_streak"])