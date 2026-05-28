from database import save_trigger_entry

def save_and_format_trigger(
    telegram_id: int,
    situation: str,
    thought: str,
    emotion: str,
    body_reaction: str,
    impulse: str,
    need: str,
) -> str:
    """Сохраняет разбор триггера в БД и возвращает текст с анализом для пользователя."""
    save_trigger_entry(
        telegram_id=telegram_id,
        situation=situation,
        thought=thought,
        emotion=emotion,
        body=body_reaction,      # в БД поле называется body
        impulse=impulse,
        need=need,
    )

    response = (
        "Готово. Я сохранил разбор триггера 🧠\n\n"
        "Вот цепочка, которую мы увидели:\n\n"
        f"Ситуация: {situation}\n"
        f"Мысль: {thought}\n"
        f"Эмоция: {emotion}\n"
        f"Тело: {body_reaction}\n"
        f"Импульс: {impulse}\n"
        f"Потребность: {need}\n\n"
        "Мягкий вывод:\n"
        "Похоже, тебя задела не только сама ситуация, а то значение, которое мозг ей придал. "
        "Это не значит, что с тобой что-то не так. Это сигнал, что была важная потребность.\n\n"
        "Что можно сделать сейчас:\n"
        "1. Сделать паузу 5–10 минут.\n"
        "2. Не действовать на пике эмоции.\n"
        "3. Спросить себя: «Какой самый бережный следующий шаг?»\n\n"
        "Если состояние всё ещё сильное, можно нажать 🆘 «Меня накрыло»."
    )
    return response