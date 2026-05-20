import os
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

AI_API_KEY = os.getenv("AI_API_KEY")
AI_BASE_URL = os.getenv("AI_BASE_URL", "https://api.vsegpt.ru/v1")
AI_MODEL = os.getenv("AI_MODEL", "deepseek/deepseek-chat")

AI_ENABLED = bool(AI_API_KEY)
