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
            KeyboardButton(text="🌬 Дыхание 4–6"),
            KeyboardButton(text="👀 5–4–3–2–1"),
        ],
        [
            KeyboardButton(text="🛑 STOP"),
            KeyboardButton(text="✍️ Письмо без отправки"),
        ],
        [
            KeyboardButton(text="🎯 Зона контроля"),
            KeyboardButton(text="💛 Самосострадание"),
        ],
        [
            KeyboardButton(text="⬅️ Главное меню"),
        ],
    ],
    resize_keyboard=True
)


from texts import CONSENT_ACCEPT_BUTTON, CONSENT_DECLINE_BUTTON


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