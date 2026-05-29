from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from services.i18n import get_text

def _btn(key: str, lang: str) -> KeyboardButton:
    return KeyboardButton(text=get_text(key, lang))

def get_focus_menu(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [_btn("focus_anxiety_button", lang)],
            [_btn("focus_relationships_button", lang)],
            [_btn("focus_relax_button", lang)],
            [_btn("focus_diary_button", lang)],
            [_btn("focus_other_button", lang)],
        ],
        resize_keyboard=True
    )

def get_main_menu(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [_btn("sos_button_text", lang), _btn("talk_button_text", lang)],
            [_btn("trigger_button_text", lang), _btn("relationships_button_text", lang)],
            [_btn("diary_button_text", lang), _btn("exercises_button_text", lang)],
            [_btn("map_button_text", lang), _btn("settings_button_text", lang)],
            [_btn("garden_button", lang)],
        ],
        resize_keyboard=True
    )

def get_sos_menu(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [_btn("sos_anxiety", lang), _btn("sos_panic", lang)],
            [_btn("sos_anger", lang), _btn("sos_cry", lang)],
            [_btn("sos_loneliness", lang), _btn("sos_sleep", lang)],
            [_btn("back_to_main_menu_button", lang)],
        ],
        resize_keyboard=True
    )

def get_relationships_menu(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [_btn("rel_ignored", lang), _btn("rel_jealousy", lang)],
            [_btn("rel_cold_partner", lang), _btn("rel_cannot_let_go", lang)],
            [_btn("rel_conflicts", lang), _btn("rel_boundary", lang)],
            [_btn("rel_help_write", lang)],
            [_btn("back_to_main_menu_button", lang)],
        ],
        resize_keyboard=True
    )

def get_exercises_menu(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [_btn("breathing_46_button", lang), _btn("grounding_button", lang)],
            [_btn("stop_button", lang), _btn("unsent_letter_button", lang)],
            [_btn("control_zone_button", lang), _btn("self_compassion_button", lang)],
            [_btn("breathing_button", lang)],
            [_btn("back_to_main_menu_button", lang)],
        ],
        resize_keyboard=True
    )

def get_onboarding_menu(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [_btn("consent_accept_button", lang)],
            [_btn("consent_decline_button", lang)],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder=get_text("confirm_age_placeholder", lang),
    )

def get_settings_menu(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [_btn("settings_rules_button", lang)],
            [_btn("settings_privacy_button", lang)],
            [_btn("settings_withdraw_consent_button", lang)],
            [_btn("settings_delete_data_button", lang)],
            [_btn("daily_reminder_button", lang)],
            [_btn("reminder_disable_button", lang)],
            [_btn("change_focus_button", lang)],
            [_btn("crisis_plan_button", lang)],
            [_btn("language_button", lang)],
            [_btn("settings_back_button", lang)],
        ],
        resize_keyboard=True,
        input_field_placeholder=get_text("settings_placeholder", lang),
    )

def get_delete_data_confirm_menu(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [_btn("delete_data_confirm_button", lang)],
            [_btn("settings_cancel_button", lang)],
        ],
        resize_keyboard=True,
        input_field_placeholder=get_text("confirm_delete_placeholder", lang),
    )

def get_withdraw_consent_confirm_menu(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [_btn("withdraw_consent_confirm_button", lang)],
            [_btn("settings_cancel_button", lang)],
        ],
        resize_keyboard=True,
        input_field_placeholder=get_text("confirm_withdraw_placeholder", lang),
    )

# Инлайн-клавиатуры оставим пока старыми (для упражнений), так как их текст не критичен для первого этапа.
# При необходимости их тоже можно перевести.
from texts import FAST_MOOD_EMOJI_MAP   # пока используем старый импорт

def breathing_continue_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Продолжить", callback_data="breathing_next")],
        [InlineKeyboardButton(text="🔊 Прослушать", callback_data="listen")],
        [InlineKeyboardButton(text="🚪 Выйти", callback_data="breathing_exit")],
    ])

def breathing_finish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вернуться в меню", callback_data="breathing_exit")],
        [InlineKeyboardButton(text="🔊 Прослушать", callback_data="listen")],
    ])

def grounding_continue_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Продолжить", callback_data="grounding_next")],
        [InlineKeyboardButton(text="🔊 Прослушать", callback_data="listen")],
        [InlineKeyboardButton(text="🚪 Выйти", callback_data="grounding_exit")],
    ])

def grounding_finish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="grounding_exit")],
        [InlineKeyboardButton(text="🔊 Прослушать", callback_data="listen")],
    ])

def stop_continue_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Продолжить", callback_data="stop_next")],
        [InlineKeyboardButton(text="🔊 Прослушать", callback_data="listen")],
        [InlineKeyboardButton(text="🚪 Выйти", callback_data="stop_exit")],
    ])

def stop_finish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="stop_exit")],
        [InlineKeyboardButton(text="🔊 Прослушать", callback_data="listen")],
    ])

def control_zone_continue_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Продолжить", callback_data="control_zone_next")],
        [InlineKeyboardButton(text="🔊 Прослушать", callback_data="listen")],
        [InlineKeyboardButton(text="🚪 Выйти", callback_data="control_zone_exit")],
    ])

def control_zone_finish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="control_zone_exit")],
        [InlineKeyboardButton(text="🔊 Прослушать", callback_data="listen")],
    ])

def self_compassion_continue_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Продолжить", callback_data="self_compassion_next")],
        [InlineKeyboardButton(text="🔊 Прослушать", callback_data="listen")],
        [InlineKeyboardButton(text="🚪 Выйти", callback_data="self_compassion_exit")],
    ])

def self_compassion_finish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="self_compassion_exit")],
        [InlineKeyboardButton(text="🔊 Прослушать", callback_data="listen")],
    ])

def unsent_letter_continue_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Продолжить", callback_data="unsent_letter_next")],
        [InlineKeyboardButton(text="🔊 Прослушать", callback_data="listen")],
        [InlineKeyboardButton(text="🚪 Выйти", callback_data="unsent_letter_exit")],
    ])

def unsent_letter_finish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="unsent_letter_exit")],
        [InlineKeyboardButton(text="🔊 Прослушать", callback_data="listen")],
    ])

def breathing46_continue_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Продолжить", callback_data="breathing46_next")],
        [InlineKeyboardButton(text="🔊 Прослушать", callback_data="listen")],
        [InlineKeyboardButton(text="🚪 Выйти", callback_data="breathing46_exit")],
    ])

def breathing46_finish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="breathing46_exit")],
        [InlineKeyboardButton(text="🔊 Прослушать", callback_data="listen")],
    ])

def fast_mood_keyboard():
    buttons = []
    row = []
    for emoji_text, _ in FAST_MOOD_EMOJI_MAP.items():
        row.append(InlineKeyboardButton(text=emoji_text, callback_data=f"fast_mood_{emoji_text}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def diary_mode_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⚡ Быстрая отметка")],
            [KeyboardButton(text="📝 Полный дневник")],
            [KeyboardButton(text="❌ Отмена")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )