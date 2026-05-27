import tempfile
import os
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from database import get_diary_entries, get_trigger_entries

router = Router()

def _safe_get(row, key, default=""):
    """Безопасно получает значение из sqlite3.Row по ключу."""
    try:
        return row[key] if key in row.keys() else default
    except:
        return default

def _format_diary(entries) -> str:
    if not entries:
        return "Нет записей дневника.\n"
    lines = ["=== ДНЕВНИК ==="]
    for row in entries:
        date_str = _safe_get(row, "created_at")
        mood = _safe_get(row, "mood") or _safe_get(row, "mood_score")
        anxiety = _safe_get(row, "anxiety") or _safe_get(row, "anxiety_score")
        energy = _safe_get(row, "energy") or _safe_get(row, "energy_score")
        sleep = _safe_get(row, "sleep_quality") or _safe_get(row, "sleep")
        note = _safe_get(row, "note")
        lines.append(f"Дата: {date_str}")
        lines.append(f"  Настроение: {mood}/10")
        lines.append(f"  Тревога: {anxiety}/10")
        lines.append(f"  Энергия: {energy}/10")
        lines.append(f"  Сон: {sleep}")
        lines.append(f"  Заметка: {note}")
        lines.append("")
    return "\n".join(lines)

def _format_triggers(entries) -> str:
    if not entries:
        return "Нет разборов триггеров.\n"
    lines = ["=== РАЗБОРЫ ТРИГГЕРОВ ==="]
    for row in entries:
        date_str = _safe_get(row, "created_at")
        situation = _safe_get(row, "situation")
        thought = _safe_get(row, "thought")
        emotion = _safe_get(row, "emotion")
        body = _safe_get(row, "body") or _safe_get(row, "body_reaction")
        impulse = _safe_get(row, "impulse")
        need = _safe_get(row, "need")
        lines.append(f"Дата: {date_str}")
        lines.append(f"  Ситуация: {situation}")
        lines.append(f"  Мысль: {thought}")
        lines.append(f"  Эмоция: {emotion}")
        lines.append(f"  Тело: {body}")
        lines.append(f"  Импульс: {impulse}")
        lines.append(f"  Потребность: {need}")
        lines.append("")
    return "\n".join(lines)

@router.message(Command("export"))
async def export_data(message: Message):
    if not message.from_user:
        await message.answer("Не смог определить пользователя.")
        return

    telegram_id = message.from_user.id
    diary = get_diary_entries(telegram_id)
    triggers = get_trigger_entries(telegram_id)

    content = "ЭКСПОРТ ДАННЫХ ОПОРА AI\n\n"
    content += _format_diary(diary)
    content += "\n\n"
    content += _format_triggers(triggers)

    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".txt") as f:
        f.write(content)
        f.flush()
        file_path = f.name

    try:
        await message.answer_document(FSInputFile(file_path), caption="Ваши данные экспортированы.")
    finally:
        os.unlink(file_path)