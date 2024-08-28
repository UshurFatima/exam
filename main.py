import logging
import asyncio
from aiogram import Bot
from bot_config import bot, dp, db, set_commands
from handlers.start import start_router
from handlers.survey import survey_router


def on_startup(bot: Bot):
    print('Бот запущен')
    db.create_tables()


async def main():
    await set_commands()
    dp.include_routers(start_router, survey_router)

    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
