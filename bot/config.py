import os
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN")
MAIN_MENU_PHOTO_ID: str = os.getenv("MAIN_MENU_PHOTO_ID")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN не найден. Убедись, что файл .env существует и содержит BOT_TOKEN="
    )

DEFAULT_PARSE_MODE = ParseMode.HTML
