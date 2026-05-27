from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from texts import CONSENT_ACCEPT_BUTTON, CONSENT_DECLINE_BUTTON
from texts import (
    SETTINGS_RULES_BUTTON,
    SETTINGS_PRIVACY_BUTTON,
    SETTINGS_WITHDRAW_CONSENT_BUTTON,
    SETTINGS_DELETE_DATA_BUTTON,
    SETTINGS_BACK_BUTTON,
    DELETE_DATA_CONFIRM_BUTTON,
    WITHDRAW_CONSENT_CONFIRM_BUTTON,
    SETTINGS_CANCEL_BUTTON,
    FOCUS_ANXIETY_BUTTON,
    FOCUS_RELATIONSHIPS_BUTTON,
    FOCUS_RELAX_BUTTON,
    FOCUS_DIARY_BUTTON,
    FOCUS_OTHER_BUTTON,
    DAILY_REMINDER_BUTTON,
    BREATHING_BUTTON,
    GROUNDING_BUTTON,
    REMINDER_DISABLE_BUTTON,
    STOP_BUTTON,
    CONTROL_ZONE_BUTTON,
    SELF_COMPASSION_BUTTON,
    UNSENT_LETTER_BUTTON,
    BREATHING_46_BUTTON,
)

focus_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=FOCUS_ANXIETY_BUTTON)],
        [KeyboardButton(text=FOCUS_RELATIONSHIPS_BUTTON)],
        [KeyboardButton(text=FOCUS_RELAX_BUTTON)],
        [KeyboardButton(text=FOCUS_DIARY_BUTTON)],
        [KeyboardButton(text=FOCUS_OTHER_BUTTON)],
    ],
    resize_keyboard=True
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🆘 Меня накрыло"),
            KeyboardButton(text="💬 Поговорить"),
        ],
        [
            KeyboardButton(text="🧠 Разобрать триггер"),
            KeyboardButton(text="💔 Отношения"),
        ],
        [
            KeyboardButton(text="📝 Дневник"),
            KeyboardButton(text="🌿 Упражнения"),
        ],
        [
            KeyboardButton(text="📊 Моя карта"),
            KeyboardButton(text="⚙️ Настройки"),
        ],
    ],
    resize_keyboard=True
)

sos_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="😰 Тревога"),
            KeyboardButton(text="😵 Паника"),
        ],
        [
            KeyboardButton(text="🔥 Злость"),
            KeyboardButton(text="😭 Хочется плакать"),
        ],
        [
            KeyboardButton(text="💔 Боль/одиночество"),
            KeyboardButton(text="🌙 Не могу уснуть"),
        ],
        [
            KeyboardButton(text="⬅️ Главное меню"),
        ],
    ],
    resize_keyboard=True
)

relationships_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💔 Меня игнорируют"),
            KeyboardButton(text="😡 Я ревную"),
        ],
        [
            KeyboardButton(text="🥶 Партнёр холодный"),
            KeyboardButton(text="🧲 Не могу отпустить"),
        ],
        [
            KeyboardButton(text="🧨 Мы постоянно ссоримся"),
            KeyboardButton(text="🚧 Хочу поставить границу"),
        ],
        [
            KeyboardButton(text="✉️ Помоги написать сообщение"),
        ],
        [
            KeyboardButton(text="⬅️ Главное меню"),
        ],
    ],
    resize_keyboard=True
)

exercises_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BREATHING_46_BUTTON),
            KeyboardButton(text=GROUNDING_BUTTON),
        ],
        [
            KeyboardButton(text=STOP_BUTTON),
            KeyboardButton(text=UNSENT_LETTER_BUTTON),
        ],
        [
            KeyboardButton(text=CONTROL_ZONE_BUTTON),
            KeyboardButton(text=SELF_COMPASSION_BUTTON),
        ],
        [
            KeyboardButton(text=BREATHING_BUTTON),
        ],
        [
            KeyboardButton(text="⬅️ Главное меню"),
        ],
    ],
    resize_keyboard=True
)

onboarding_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=CONSENT_ACCEPT_BUTTON)],
        [KeyboardButton(text=CONSENT_DECLINE_BUTTON)],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Подтвердите возраст и правила",
)

settings_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=SETTINGS_RULES_BUTTON)],
        [KeyboardButton(text=SETTINGS_PRIVACY_BUTTON)],
        [KeyboardButton(text=SETTINGS_WITHDRAW_CONSENT_BUTTON)],
        [KeyboardButton(text=SETTINGS_DELETE_DATA_BUTTON)],
        [KeyboardButton(text=DAILY_REMINDER_BUTTON)],
        [KeyboardButton(text=REMINDER_DISABLE_BUTTON)],
        [KeyboardButton(text=SETTINGS_BACK_BUTTON)],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт настроек",
)

delete_data_confirm_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=DELETE_DATA_CONFIRM_BUTTON)],
        [KeyboardButton(text=SETTINGS_CANCEL_BUTTON)],
    ],
    resize_keyboard=True,
    input_field_placeholder="Подтвердите удаление данных",
)

withdraw_consent_confirm_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=WITHDRAW_CONSENT_CONFIRM_BUTTON)],
        [KeyboardButton(text=SETTINGS_CANCEL_BUTTON)],
    ],
    resize_keyboard=True,
    input_field_placeholder="Подтвердите отзыв согласия",
)

# Инлайн-клавиатуры для дыхательного упражнения
def breathing_continue_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Продолжить", callback_data="breathing_next")],
        [InlineKeyboardButton(text="🚪 Выйти", callback_data="breathing_exit")],
    ])

def breathing_finish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вернуться в меню", callback_data="breathing_exit")],
    ])

# Инлайн-клавиатуры для упражнения 5-4-3-2-1
def grounding_continue_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Продолжить", callback_data="grounding_next")],
        [InlineKeyboardButton(text="🚪 Выйти", callback_data="grounding_exit")],
    ])

def grounding_finish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="grounding_exit")],
    ])

# Инлайн-клавиатуры для упражнения STOP
def stop_continue_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Продолжить", callback_data="stop_next")],
        [InlineKeyboardButton(text="🚪 Выйти", callback_data="stop_exit")],
    ])

def stop_finish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="stop_exit")],
    ])

# Инлайн-клавиатуры для Зоны контроля
def control_zone_continue_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Продолжить", callback_data="control_zone_next")],
        [InlineKeyboardButton(text="🚪 Выйти", callback_data="control_zone_exit")],
    ])

def control_zone_finish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="control_zone_exit")],
    ])

# Инлайн-клавиатуры для Самосострадания
def self_compassion_continue_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Продолжить", callback_data="self_compassion_next")],
        [InlineKeyboardButton(text="🚪 Выйти", callback_data="self_compassion_exit")],
    ])

def self_compassion_finish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="self_compassion_exit")],
    ])

# Инлайн-клавиатуры для Письма без отправки
def unsent_letter_continue_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Продолжить", callback_data="unsent_letter_next")],
        [InlineKeyboardButton(text="🚪 Выйти", callback_data="unsent_letter_exit")],
    ])

def unsent_letter_finish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="unsent_letter_exit")],
    ])

# Инлайн-клавиатуры для Дыхания 4–6
def breathing46_continue_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Продолжить", callback_data="breathing46_next")],
        [InlineKeyboardButton(text="🚪 Выйти", callback_data="breathing46_exit")],
    ])

def breathing46_finish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="breathing46_exit")],
    ])