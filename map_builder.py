import re
from collections import Counter

from database import (
    get_diary_entries,
    get_diary_stats,
    get_sleep_stats,
    get_trigger_entries,
    get_trigger_count,
)


THEME_KEYWORDS = {
    "работа": [
        "работа",
        "работе",
        "работу",
        "работой",
        "начальник",
        "коллега",
        "коллеги",
        "задача",
        "дедлайн",
        "проект",
    ],
    "отношения": [
        "отношения",
        "партнер",
        "партнёр",
        "муж",
        "жена",
        "парень",
        "девушка",
        "любимый",
        "любимая",
        "расстались",
        "игнор",
        "ревность",
        "ссора",
    ],
    "семья": [
        "семья",
        "мама",
        "папа",
        "родители",
        "ребенок",
        "ребёнок",
        "дети",
        "сын",
        "дочь",
        "брат",
        "сестра",
    ],
    "тревога": [
        "тревога",
        "тревожно",
        "страх",
        "боюсь",
        "паника",
        "переживаю",
        "нервничаю",
        "напряжение",
    ],
    "усталость": [
        "устал",
        "устала",
        "усталость",
        "выгорел",
        "выгорела",
        "нет сил",
        "изнеможение",
        "обессилен",
        "обессилена",
    ],
    "сон": [
        "сон",
        "спал",
        "спала",
        "не спал",
        "не спала",
        "бессонница",
        "уснуть",
        "проснулся",
        "проснулась",
    ],
    "деньги": [
        "деньги",
        "финансы",
        "зарплата",
        "долг",
        "кредит",
        "ипотека",
        "расходы",
        "доход",
    ],
    "конфликт": [
        "конфликт",
        "ссора",
        "поругались",
        "ругались",
        "крик",
        "кричал",
        "кричала",
        "обида",
        "злость",
    ],
    "одиночество": [
        "одиноко",
        "одиночество",
        "одна",
        "один",
        "никому не нужен",
        "никому не нужна",
        "нет поддержки",
    ],
}


STOP_WORDS = {
    "это",
    "как",
    "так",
    "что",
    "все",
    "всё",
    "мне",
    "меня",
    "мой",
    "моя",
    "мои",
    "мое",
    "моё",
    "тебя",
    "его",
    "она",
    "оно",
    "они",
    "мы",
    "вы",
    "нас",
    "вам",
    "для",
    "при",
    "над",
    "под",
    "или",
    "если",
    "но",
    "да",
    "нет",
    "уже",
    "еще",
    "ещё",
    "там",
    "тут",
    "тогда",
    "сейчас",
    "очень",
    "просто",
    "было",
    "была",
    "были",
    "будет",
    "будто",
    "потому",
    "когда",
    "после",
    "перед",
    "себя",
    "себе",
    "тоже",
    "только",
    "из-за",
    "изза",
    "про",
    "без",
    "надо",
    "нужно",
    "хочу",
    "хотел",
    "хотела",
}


def _get_value(row, key, index=None, default=""):
    """
    Достаёт значение из разных форматов:
    - dict
    - sqlite3.Row
    - tuple/list
    """
    if row is None:
        return default

    try:
        if isinstance(row, dict):
            return row.get(key, default)
    except Exception:
        pass

    try:
        return row[key]
    except Exception:
        pass

    if index is not None:
        try:
            return row[index]
        except Exception:
            pass

    return default


def _to_number(value, default=0):
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def _round_1(value):
    try:
        return round(float(value), 1)
    except Exception:
        return 0


def _clean_text(text):
    if not text:
        return ""
    return str(text).lower().replace("ё", "е").strip()


def _words_from_text(text):
    text = _clean_text(text)
    words = re.findall(r"[а-яa-z]{3,}", text, flags=re.IGNORECASE)
    return [word for word in words if word not in STOP_WORDS]


def _top_words(texts, limit=7):
    counter = Counter()

    for text in texts:
        counter.update(_words_from_text(text))

    return counter.most_common(limit)


def _top_phrases(texts, limit=5):
    """
    Для коротких полей триггера считаем частые повторяющиеся ответы.
    Например: 'страх', 'злость', 'сжалось в груди'.
    """
    counter = Counter()

    for text in texts:
        cleaned = _clean_text(text)
        if len(cleaned) >= 2:
            counter[cleaned] += 1

    return counter.most_common(limit)


def _theme_counts(texts):
    joined_text = " ".join(_clean_text(text) for text in texts)
    result = Counter()

    for theme, keywords in THEME_KEYWORDS.items():
        count = 0
        for keyword in keywords:
            keyword = keyword.lower().replace("ё", "е")
            count += joined_text.count(keyword)
        if count > 0:
            result[theme] = count

    return result.most_common(5)


def _format_top_items(items, empty_text="Пока недостаточно данных."):
    if not items:
        return f"— {empty_text}"

    lines = []
    for item, count in items:
        if count > 1:
            lines.append(f"— {item} — {count} раза")
        else:
            lines.append(f"— {item}")

    return "\n".join(lines)


def _extract_diary_data(diary_entries):
    """
    Таблица diary_entries:
    0 id
    1 telegram_id
    2 mood_score
    3 anxiety_score
    4 energy_score
    5 sleep_quality
    6 note
    7 created_at
    """
    moods = []
    anxieties = []
    energies = []
    sleep_values = []
    notes = []

    for row in diary_entries:
        mood = _get_value(row, "mood_score", 2, None)
        anxiety = _get_value(row, "anxiety_score", 3, None)
        energy = _get_value(row, "energy_score", 4, None)
        sleep = _get_value(row, "sleep_quality", 5, "")
        note = _get_value(row, "note", 6, "")

        if mood is not None:
            moods.append(_to_number(mood))
        if anxiety is not None:
            anxieties.append(_to_number(anxiety))
        if energy is not None:
            energies.append(_to_number(energy))
        if sleep:
            sleep_values.append(str(sleep))
        if note:
            notes.append(str(note))

    return moods, anxieties, energies, sleep_values, notes


def _extract_trigger_data(trigger_entries):
    """
    Таблица trigger_entries:
    0 id
    1 telegram_id
    2 situation
    3 thought
    4 emotion
    5 body_reaction
    6 impulse
    7 need
    8 created_at
    """
    situations = []
    thoughts = []
    emotions = []
    body_reactions = []
    impulses = []
    needs = []

    for row in trigger_entries:
        situation = _get_value(row, "situation", 2, "")
        thought = _get_value(row, "thought", 3, "")
        emotion = _get_value(row, "emotion", 4, "")
        body_reaction = _get_value(row, "body_reaction", 5, "")
        impulse = _get_value(row, "impulse", 6, "")
        need = _get_value(row, "need", 7, "")

        if situation:
            situations.append(str(situation))
        if thought:
            thoughts.append(str(thought))
        if emotion:
            emotions.append(str(emotion))
        if body_reaction:
            body_reactions.append(str(body_reaction))
        if impulse:
            impulses.append(str(impulse))
        if need:
            needs.append(str(need))

    return situations, thoughts, emotions, body_reactions, impulses, needs


def _make_soft_summary(avg_mood, avg_anxiety, avg_energy, trigger_count):
    parts = []

    if avg_anxiety >= 7:
        parts.append(
            "Похоже, в последнее время тревога занимает много места. "
            "Сейчас особенно важны стабилизация, сон, паузы и снижение нагрузки."
        )
    elif avg_anxiety >= 4:
        parts.append(
            "Тревога присутствует, но её уже можно исследовать: "
            "что её запускает, какие мысли появляются и какая поддержка помогает."
        )
    else:
        parts.append(
            "По дневнику тревога не выглядит очень высокой. "
            "Можно мягко укреплять то, что уже помогает держаться устойчивее."
        )

    if avg_mood <= 4:
        parts.append(
            "Настроение выглядит сниженным. Важно не требовать от себя слишком много "
            "и добавлять маленькие действия восстановления."
        )
    elif avg_mood >= 7:
        parts.append(
            "Настроение в среднем выглядит довольно устойчивым. "
            "Полезно замечать, какие действия и условия этому помогают."
        )

    if avg_energy <= 4:
        parts.append(
            "Энергии немного. Возможно, сейчас полезнее не 'собраться любой ценой', "
            "а бережно восстановить ресурс."
        )

    if trigger_count >= 3:
        parts.append(
            "Уже есть несколько разборов триггеров — это хорошая база, "
            "чтобы замечать повторяющиеся сценарии, а не винить себя за реакции."
        )

    return "\n\n".join(parts)


def _make_week_focus(
    avg_anxiety,
    avg_energy,
    themes,
    situations,
    thoughts,
    emotions,
    needs,
):
    all_trigger_text = " ".join(
        situations + thoughts + emotions + needs
    ).lower().replace("ё", "е")

    theme_names = [theme for theme, _count in themes]

    # Отношения / игнор / ревность
    if (
        "отношения" in theme_names
        or "игнор" in all_trigger_text
        or "ревн" in all_trigger_text
        or "партнер" in all_trigger_text
        or "партнёр" in all_trigger_text
    ):
        return (
            "На эту неделю фокус может быть таким: перед важным сообщением или разговором "
            "делать паузу 10–20 минут, сначала стабилизироваться, а потом писать из позиции "
            "ясности: «что я чувствую, что мне важно, о чём я прошу»."
        )

    # Работа / выгорание / границы
    if (
        "работа" in theme_names
        or "усталость" in theme_names
        or "дедлайн" in all_trigger_text
        or "начальник" in all_trigger_text
    ):
        return (
            "На эту неделю фокус может быть таким: замечать моменты перегруза и тренировать "
            "маленькие границы — пауза, уточнение сроков, отказ от лишней задачи или короткий отдых."
        )

    # Безопасность / ясность / поддержка
    if (
        "безопас" in all_trigger_text
        or "ясност" in all_trigger_text
        or "поддерж" in all_trigger_text
        or "пониман" in all_trigger_text
    ):
        return (
            "На эту неделю фокус может быть таким: тренировать просьбы и прояснение. "
            "Например: «Мне важно понять…», «Мне нужна поддержка в…», "
            "«Можешь сказать прямо, что ты имеешь в виду?»"
        )

    # Высокая тревога
    if avg_anxiety >= 7:
        return (
            "На эту неделю фокус может быть таким: не разбирать всё сразу, "
            "а сначала снижать уровень тревоги — дыхание 4–6, заземление 5–4–3–2–1, "
            "сон и минимизация перегруза."
        )

    # Низкая энергия
    if avg_energy <= 4:
        return (
            "На эту неделю фокус может быть таким: восстановление энергии. "
            "Один маленький шаг в день: сон, еда, вода, прогулка, меньше самокритики."
        )

    return (
        "На эту неделю фокус может быть таким: продолжать наблюдать за связкой "
        "«ситуация → мысль → эмоция → тело → имп��льс → потребность» и записывать "
        "повторяющиеся реакции без самокритики."
    )


def build_user_map(telegram_id: int) -> str:
    diary_entries = get_diary_entries(telegram_id)
    trigger_entries = get_trigger_entries(telegram_id)

    diary_count = len(diary_entries) if diary_entries else 0

    try:
        trigger_count = get_trigger_count(telegram_id)
    except Exception:
        trigger_count = len(trigger_entries) if trigger_entries else 0

    if trigger_count is None:
        trigger_count = len(trigger_entries) if trigger_entries else 0

    # На всякий случай приводим к int
    try:
        trigger_count = int(trigger_count)
    except Exception:
        trigger_count = len(trigger_entries) if trigger_entries else 0

    if diary_count == 0 and trigger_count == 0:
        return (
            "📊 Моя карта\n\n"
            "Пока у меня мало данных, чтобы собрать твою карту.\n\n"
            "Можно начать с двух простых шагов:\n"
            "— 📝 вести дневник состояния;\n"
            "— 🧠 разбирать триггеры.\n\n"
            "Через несколько записей здесь появятся повторяющиеся темы, "
            "эмоции, потребности и мягкий фокус на неделю."
        )

    moods, anxieties, energies, sleep_values, notes = _extract_diary_data(diary_entries)
    situations, thoughts, emotions, body_reactions, impulses, needs = _extract_trigger_data(
        trigger_entries
    )

    avg_mood = _round_1(sum(moods) / len(moods)) if moods else 0
    avg_anxiety = _round_1(sum(anxieties) / len(anxieties)) if anxieties else 0
    avg_energy = _round_1(sum(energies) / len(energies)) if energies else 0

    sleep_counter = Counter(sleep_values)
    sleep_top = sleep_counter.most_common()

    all_diary_texts = notes
    all_trigger_texts = situations + thoughts + emotions + body_reactions + impulses + needs
    all_texts = all_diary_texts + all_trigger_texts

    themes = _theme_counts(all_texts)
    frequent_words = _top_words(all_texts, limit=7)

    top_situations = _top_phrases(situations, limit=5)
    top_thoughts = _top_phrases(thoughts, limit=5)
    top_emotions = _top_phrases(emotions, limit=5)
    top_body = _top_phrases(body_reactions, limit=5)
    top_impulses = _top_phrases(impulses, limit=5)
    top_needs = _top_phrases(needs, limit=5)

    summary = _make_soft_summary(
        avg_mood=avg_mood,
        avg_anxiety=avg_anxiety,
        avg_energy=avg_energy,
        trigger_count=trigger_count,
    )

    week_focus = _make_week_focus(
        avg_anxiety=avg_anxiety,
        avg_energy=avg_energy,
        themes=themes,
        situations=situations,
        thoughts=thoughts,
        emotions=emotions,
        needs=needs,
    )

    text = "📊 Моя карта\n\n"

    text += "Это не диагноз и не оценка личности. Это мягкое зеркало по твоим записям: что чаще повторяется, где может быть нагрузка и на что можно опереться.\n\n"

    text += "📝 Дневник состояния:\n"
    text += f"Записей: {diary_count}\n"

    if diary_count > 0:
        text += f"Среднее настроение: {avg_mood}/10\n"
        text += f"Средняя тревога: {avg_anxiety}/10\n"
        text += f"Средняя энергия: {avg_energy}/10\n\n"

        text += "🌙 Сон:\n"
        if sleep_top:
            for sleep, count in sleep_top:
                text += f"— {sleep}: {count}\n"
        else:
            text += "— пока нет данных\n"
        text += "\n"
    else:
        text += "Пока нет записей дневника.\n\n"

    text += "🧠 Разборы триггеров:\n"
    text += f"Сохранённых разборов: {trigger_count}\n\n"

    if trigger_count > 0:
        text += "⚡ Частые ситуации:\n"
        text += _format_top_items(top_situations) + "\n\n"

        text += "💭 Повторяющиеся мысли:\n"
        text += _format_top_items(top_thoughts) + "\n\n"

        text += "❤️ Частые эмоции:\n"
        text += _format_top_items(top_emotions) + "\n\n"

        text += "🫀 Частые телесные реакции:\n"
        text += _format_top_items(top_body) + "\n\n"

        text += "🏃 Частые импульсы:\n"
        text += _format_top_items(top_impulses) + "\n\n"

        text += "🫴 Частые потребности:\n"
        text += _format_top_items(top_needs) + "\n\n"
    else:
        text += (
            "Пока нет сохранённых разборов триггеров. "
            "Когда ты сделаешь несколько разборов, здесь появятся повторяющиеся мысли, эмоции и потребности.\n\n"
        )

    text += "🔎 Частые темы:\n"
    text += _format_top_items(themes, empty_text="Пока темы не выделяются.") + "\n\n"

    text += "🔤 Частые слова:\n"
    text += _format_top_items(frequent_words, empty_text="Пока мало текста для анализа.") + "\n\n"

    text += "🌿 Мягкий вывод:\n"
    text += summary + "\n\n"

    text += "🎯 Фокус на неделю:\n"
    text += week_focus + "\n\n"

    text += (
        "Если в какой-то момент появляются мысли о самоповреждении, суициде, насилии "
        "или ощущение, что ты можешь потерять контроль, важно сразу обратиться за срочной помощью "
        "к близкому человеку, врачу или в экстренные службы."
    )

    return text