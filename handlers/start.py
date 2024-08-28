from aiogram import types, Router
from aiogram.filters.command import Command

start_router = Router()


@start_router.message(Command('start'))
async def start_handler(message: types.Message):
    await message.answer('Здравствуйте! Этот бот проводит короткий опрос о вас')
