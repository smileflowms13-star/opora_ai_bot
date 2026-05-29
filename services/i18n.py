from locales import ru, en, hi, zh

LANGUAGES = {
    "ru": ru.TEXTS,
    "en": en.TEXTS,
    "hi": hi.TEXTS,
    "zh": zh.TEXTS,
}

FALLBACK_LANG = "ru"

def get_text(key: str, lang: str = None) -> str:
    if not lang or lang not in LANGUAGES:
        lang = FALLBACK_LANG
    return LANGUAGES.get(lang, LANGUAGES[FALLBACK_LANG]).get(key, key)