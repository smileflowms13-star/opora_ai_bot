# Opora AI Bot

Telegram-бот на Python с использованием aiogram и OpenAI-совместимого AI API.

## Возможности

- Telegram-бот на aiogram 3
- Ответы через AI API, если настроен AI-ключ
- Локальная база данных SQLite
- Логирование работы приложения
- Настройка через файл `.env`

## Требования

- Python 3.10 или новее
- Telegram bot token от BotFather
- AI API key — необязательно, нужен только для AI-ответов

## Установка

Создать виртуальное окружение:

```powershell
python -m venv .venv
```

Активировать виртуальное окружение:

```powershell
.\.venv\Scripts\Activate.ps1
```

Установить зависимости:

```powershell
python -m pip install -r requirements.txt
```

## Настройка

Создать локальный файл `.env` из примера:

```powershell
Copy-Item .env.example .env
```

Потом открыть файл `.env` и вписать настоящие значения.

Файл `.env` нельзя коммитить в Git, потому что в нём хранятся секреты.

## Переменные окружения

| Переменная | Обязательная | Описание |
|---|---:|---|
| `BOT_TOKEN` | Да | Токен Telegram-бота от BotFather |
| `AI_API_KEY` | Нет | Ключ для AI API |
| `AI_BASE_URL` | Нет | Адрес OpenAI-совместимого AI API |
| `AI_MODEL` | Нет | Название AI-модели |

Значения по умолчанию для AI указаны в файле `config.py`.

## Запуск

Запустить бота:

```powershell
python bot.py
```

После запуска открой Telegram и отправь боту команду:

```text
/start
```

## Основные файлы проекта

- `bot.py` — точка входа, запуск бота
- `config.py` — чтение настроек из `.env`
- `ai_client.py` — работа с AI API
- `database.py` — работа с SQLite-базой
- `handlers/` — обработчики сообщений Telegram
- `logger_config.py` — настройка логирования
- `.env.example` — пример файла настроек без секретов
- `requirements.txt` — зафиксированные зависимости Python

## Безопасность

- Не коммить файл `.env`
- Не публикуй реальные токены и API-ключи
- Не добавляй в Git локальную базу данных и логи
