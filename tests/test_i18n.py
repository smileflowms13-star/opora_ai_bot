from services.i18n import get_text

def test_get_text_ru():
    assert get_text("sos_button_text", "ru") == "🆘 Меня накрыло"

def test_get_text_en():
    assert get_text("sos_button_text", "en") == "🆘 I'm overwhelmed"

def test_get_text_fallback():
    # неизвестный язык — должен вернуть русский
    assert get_text("sos_button_text", "fr") == "🆘 Меня накрыло"

def test_get_text_missing_key():
    # Если ключа нет нигде, возвращается сам ключ
    assert get_text("nonexistent_key", "ru") == "nonexistent_key"