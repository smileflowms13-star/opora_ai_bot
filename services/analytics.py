from database import get_diary_entries
from datetime import date, timedelta

QUICK_SUGGEST_MAP = {
    "тревог": ["Дыхание 4–6", "5-4-3-2-1"],
    "тревож": ["Дыхание 4–6", "5-4-3-2-1"],
    "паник": ["Дыхание 4–6", "STOP"],
    "злост": ["STOP", "Письмо без отправки"],
    "злю": ["STOP", "Письмо без отправки"],
    "груст": ["Самосострадание", "Письмо без отправки"],
    "одино": ["Самосострадание", "Письмо без отправки"],
    "не могу уснуть": ["Дыхание 4–6", "Самосострадание"],
    "бессонниц": ["Дыхание 4–6", "Самосострадание"],
    "стресс": ["STOP", "Дыхание 4–6"],
    "напряж": ["Дыхание 4–6", "5-4-3-2-1"],
    "устал": ["Зона контроля", "Самосострадание"],
    "нет сил": ["Зона контроля", "Самосострадание"],
    "выгорел": ["Зона контроля", "Самосострадание"],
    "плач": ["Самосострадание", "STOP"],
    "обид": ["Письмо без отправки", "Самосострадание"],
    "обижен": ["Письмо без отправки", "Самосострадание"],
    "страх": ["5-4-3-2-1", "Дыхание 4–6"],
    "боль": ["Самосострадание", "STOP"],
    "накрыло": ["STOP", "5-4-3-2-1"],
    "не контролиру": ["STOP", "Зона контроля"],
    "контроль теря": ["STOP", "Зона контроля"],
}


def get_personalized_suggestion(telegram_id: int) -> str:
    """Анализирует дневник за 7 дней и возвращает персональную рекомендацию."""
    diary_entries = get_diary_entries(telegram_id)

    if not diary_entries:
        return "У меня пока недостаточно данных, чтобы предложить что-то персональное. Начни вести дневник, и я смогу анализировать твоё состояние."

    week_ago = date.today() - timedelta(days=7)
    recent = []
    for row in diary_entries:
        created_str = row["created_at"] if "created_at" in row.keys() else ""
        if created_str:
            try:
                created_date = date.fromisoformat(created_str[:10])
                if created_date >= week_ago:
                    recent.append(row)
            except:
                continue

    if not recent:
        return "За последнюю неделю нет новых записей в дневнике. Чтобы я мог дать совет, запиши хотя бы пару наблюдений."

    moods, anxieties, energies = [], [], []
    for row in recent:
        mood = row["mood"] if "mood" in row.keys() else row.get("mood_score", None)
        anxiety = row["anxiety"] if "anxiety" in row.keys() else row.get("anxiety_score", None)
        energy = row["energy"] if "energy" in row.keys() else row.get("energy_score", None)
        if mood is not None:
            try: moods.append(float(mood))
            except: pass
        if anxiety is not None:
            try: anxieties.append(float(anxiety))
            except: pass
        if energy is not None:
            try: energies.append(float(energy))
            except: pass

    avg_mood = sum(moods) / len(moods) if moods else None
    avg_anxiety = sum(anxieties) / len(anxieties) if anxieties else None
    avg_energy = sum(energies) / len(energies) if energies else None

    if avg_anxiety is not None and avg_anxiety >= 7:
        return ("За последнюю неделю тревога держится на высоком уровне. "
                "Попробуй технику «Дыхание 4–6» — она помогает быстро снизить напряжение. "
                "Нажми 🌬️ Дыхание 4–6 в меню упражнений.")
    if avg_energy is not None and avg_energy <= 3:
        return ("Похоже, энергии сейчас совсем мало. Это нормально, не требуй от себя максимума. "
                "Сделай что-то маленькое и бережное: выйди на 5 минут на воздух, выпей воды, "
                "или попробуй упражнение «Самосострадание».")
    if avg_mood is not None and avg_mood <= 4:
        return ("Настроение в последние дни снижено. Это сигнал, что тебе нужна поддержка. "
                "Попробуй «Письмо без отправки» — оно поможет выразить эмоции, не держа их в себе.")
    if avg_anxiety is not None and 4 <= avg_anxiety < 7:
        return ("Тревога присутствует, но не на пике. Попробуй «STOP» — он поможет заземлиться в моменте. "
                "Или просто поговори со мной о том, что тебя беспокоит.")
    if avg_energy is not None and 4 <= avg_energy < 6:
        return ("Энергия средняя. Возможно, полезно переключиться на что-то приятное. "
                "Попробуй «Зону контроля» — она помогает разделить заботы на подконтрольные и неподвластные, возвращая ясность.")
    if avg_mood is not None and avg_mood >= 7:
        return ("Настроение в среднем устойчивое! Отлично. Может быть, сейчас хороший момент "
                "для практики благодарности или просто отметить, что помогает тебе оставаться в ресурсе.")

    return ("По последним записям твоё состояние в целом стабильно. "
            "Продолжай наблюдать за собой и возвращайся к упражнениям по необходимости.")


def get_quick_exercise_suggestions(text: str) -> list[str] | None:
    """
    Быстрый подбор упражнений по ключевым словам в сообщении.
    Возвращает список названий упражнений или None, если ничего не найдено.
    """
    if not text:
        return None
    normalized = text.lower().replace("ё", "е")
    for keyword, exercises in QUICK_SUGGEST_MAP.items():
        if keyword in normalized:
            return exercises
    return None