import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand

from .config import BOT_TOKEN, DEFAULT_PARSE_MODE
from . import handlers


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(
        BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=DEFAULT_PARSE_MODE),
    )
    dp = Dispatcher()

    # Подключаем все роутеры
    dp.include_router(handlers.start.router)
    dp.include_router(handlers.pay.router)
    dp.include_router(handlers.info.router)
    dp.include_router(handlers.instruction.router)
    dp.include_router(handlers.referral.router)
    dp.include_router(handlers.settings.router)

    # Команды бота
    await bot.set_my_commands(
        [
            BotCommand(command="menu", description="Главное меню"),
        ]
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
