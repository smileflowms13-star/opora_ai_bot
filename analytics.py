from database import get_diary_entries
from datetime import date, timedelta

def get_personalized_suggestion(telegram_id: int) -> str:
    """
    Анализирует дневник за 7 дней и возвращает персонализированную рекомендацию.
    """
    diary_entries = get_diary_entries(telegram_id)

    if not diary_entries:
        return "У меня пока недостаточно данных, чтобы предложить что-то персональное. Начни вести дневник, и я смогу анализировать твоё состояние."

    # Фильтруем за последние 7 дней
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

    # Собираем средние показатели
    moods, anxieties, energies = [], [], []
    for row in recent:
        mood = row["mood"] if "mood" in row.keys() else row["mood_score"] if "mood_score" in row.keys() else None
        anxiety = row["anxiety"] if "anxiety" in row.keys() else row["anxiety_score"] if "anxiety_score" in row.keys() else None
        energy = row["energy"] if "energy" in row.keys() else row["energy_score"] if "energy_score" in row.keys() else None
        if mood is not None:
            try:
                moods.append(float(mood))
            except:
                pass
        if anxiety is not None:
            try:
                anxieties.append(float(anxiety))
            except:
                pass
        if energy is not None:
            try:
                energies.append(float(energy))
            except:
                pass

    avg_mood = sum(moods) / len(moods) if moods else None
    avg_anxiety = sum(anxieties) / len(anxieties) if anxieties else None
    avg_energy = sum(energies) / len(energies) if energies else None

    # Логика рекомендаций
    if avg_anxiety is not None and avg_anxiety >= 7:
        return (
            "За последнюю неделю тревога держится на высоком уровне. "
            "Попробуй технику «Дыхание 4–6» — она помогает быстро снизить напряжение. "
            "Нажми 🌬️ Дыхание 4–6 в меню упражнений."
        )
    if avg_energy is not None and avg_energy <= 3:
        return (
            "Похоже, энергии сейчас совсем мало. Это нормально, не требуй от себя максимума. "
            "Сделай что-то маленькое и бережное: выйди на 5 минут на воздух, выпей воды, "
            "или попробуй упражнение «Самосострадание»."
        )
    if avg_mood is not None and avg_mood <= 4:
        return (
            "Настроение в последние дни снижено. Это сигнал, что тебе нужна поддержка. "
            "Попробуй «Письмо без отправки» — оно поможет выразить эмоции, не держа их в себе."
        )
    if avg_anxiety is not None and 4 <= avg_anxiety < 7:
        return (
            "Тревога присутствует, но не на пике. Попробуй «STOP» — он поможет заземлиться в моменте. "
            "Или просто поговори со мной о том, что тебя беспокоит."
        )
    if avg_energy is not None and 4 <= avg_energy < 6:
        return (
            "Энергия средняя. Возможно, полезно переключиться на что-то приятное. "
            "Попробуй «Зону контроля» — она помогает разделить заботы на可控 и неподвластное, возвращая ясность."
        )
    if avg_mood is not None and avg_mood >= 7:
        return (
            "Настроение в среднем устойчивое! Отлично. Может быть, сейчас хороший момент "
            "для практики благодарности или просто отметить, что помогает тебе оставаться в ресурсе."
        )

    # Если всё в норме
    return (
        "По последним записям твоё состояние в целом стабильно. "
        "Продолжай наблюдать за собой и возвращайся к упражнениям по необходимости."
    )