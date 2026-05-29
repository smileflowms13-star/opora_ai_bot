import io
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from database import get_diary_entries, get_trigger_entries
from services.i18n import get_text
from keyboards import get_main_menu

router = Router()

def _build_export_text(telegram_id: int, lang: str) -> str:
    diary = get_diary_entries(telegram_id)
    triggers = get_trigger_entries(telegram_id)
    parts = [get_text("export_header", lang)]
    parts.append("\n" + get_text("export_diary_section", lang))
    if diary:
        for row in diary:
            date = row["created_at"] if "created_at" in row.keys() else "?"
            mood = row.get("mood") or row.get("mood_score") or "—"
            anxiety = row.get("anxiety") or row.get("anxiety_score") or "—"
            energy = row.get("energy") or row.get("energy_score") or "—"
            sleep = row.get("sleep_quality") or row.get("sleep") or "—"
            note = row.get("note") or ""
            parts.append(
                f"{date} | {get_text('export_mood', lang)} {mood} | {get_text('export_anxiety', lang)} {anxiety} | {get_text('export_energy', lang)} {energy} | {get_text('export_sleep', lang)} {sleep}"
            )
            if note:
                parts.append(f"  {get_text('export_note', lang)} {note}")
    else:
        parts.append(get_text("export_no_diary", lang))
    parts.append("\n" + get_text("export_trigger_section", lang))
    if triggers:
        for row in triggers:
            date = row["created_at"] if "created_at" in row.keys() else "?"
            situation = row.get("situation") or ""
            thought = row.get("thought") or ""
            emotion = row.get("emotion") or ""
            body = row.get("body") or row.get("body_reaction") or ""
            impulse = row.get("impulse") or ""
            need = row.get("need") or ""
            parts.append(
                f"{date}\n"
                f"  {get_text('export_situation', lang)} {situation}\n"
                f"  {get_text('export_thought', lang)} {thought}\n"
                f"  {get_text('export_emotion', lang)} {emotion}\n"
                f"  {get_text('export_body', lang)} {body}\n"
                f"  {get_text('export_impulse', lang)} {impulse}\n"
                f"  {get_text('export_need', lang)} {need}"
            )
    else:
        parts.append(get_text("export_no_triggers", lang))
    return "\n".join(parts)

@router.message(Command("export"))
async def export_command(message: Message, **kwargs):
    if not message.from_user:
        await message.answer("User not identified.")
        return
    lang = kwargs.get("lang", "ru")
    telegram_id = message.from_user.id
    text = _build_export_text(telegram_id, lang)
    file = BufferedInputFile(text.encode("utf-8"), filename=f"opora_export_{telegram_id}.txt")
    await message.answer_document(file, caption=get_text("export_caption", lang), reply_markup=get_main_menu(lang))