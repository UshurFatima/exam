from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from os import getenv
from pathlib import Path
from database.database import Database


load_dotenv()
token = getenv('BOT_TOKEN')
bot = Bot(token=token)
dp = Dispatcher()
db = Database(Path(__file__).parent / 'db.sqlite')


async def set_commands():
    await bot.set_my_commands([
        types.BotCommand(command='start', description='Начало работы'),
        types.BotCommand(command='survey', description='Начинает опрос')
    ])
