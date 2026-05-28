from typing import Optional, Tuple
from database import save_diary_entry, get_diary_stats
from services.streak_service import process_streak

def save_and_process_diary_entry(
    telegram_id: int,
    mood_score: Optional[int] = None,
    anxiety_score: Optional[int] = None,
    energy_score: Optional[int] = None,
    sleep_quality: Optional[str] = None,
    note: Optional[str] = None,
) -> Tuple[dict, Optional[str]]:
    """
    Сохраняет запись дневника и обрабатывает стрик.
    Возвращает (streak_data, streak_message).
    streak_data — словарь с текущим стриком (можно использовать, если нужно),
    но мы его здесь не используем для упрощения (можно вернуть только сообщение).
    """
    save_diary_entry(
        telegram_id=telegram_id,
        mood=mood_score,
        anxiety=anxiety_score,
        energy=energy_score,
        sleep_quality=sleep_quality,
        note=note,
    )

    streak_message = process_streak(telegram_id)
    # Для совместимости с diary.py, который ожидает кортеж, вернём (data, message).
    # data нам не нужен, но можем вернуть get_streak.
    from database import get_streak
    return get_streak(telegram_id), streak_message

def get_diary_stats_message(telegram_id: int) -> str:
    stats = get_diary_stats(telegram_id)
    if stats.get("count", 0) == 0:
        return (
            "Пока нет записей в дневнике.\n\n"
            "Нажми 📝 Дневник или напиши /diary, чтобы создать первую запись."
        )

    return (
        "📊 <b>Краткая статистика дневника</b>\n\n"
        f"Записей: {stats['count']}\n"
        f"Среднее настроение: {stats['avg_mood'] or '—'}/10\n"
        f"Средняя тревога: {stats['avg_anxiety'] or '—'}/10\n"
        f"Средняя энергия: {stats['avg_energy'] or '—'}/10\n\n"
        "Это пока простая статистика. Позже на её основе мы сделаем «Мою карту»."
    )