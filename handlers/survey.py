from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot_config import db


survey_router = Router()


class Survey(StatesGroup):
    name = State()
    age = State()
    gender = State()
    occupation = State()


@survey_router.message(Command('survey'))
async def survey_handler(message: types.Message, state: FSMContext):
    await state.set_state(Survey.name)
    await message.answer('Давайте начнем опрос. Как вас зовут?')


@survey_router.message(Survey.name)
async def name_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Survey.age)
    await message.answer('Сколько вам лет?')


@survey_router.message(Survey.age)
async def age_handler(message: types.Message, state: FSMContext):
    age = message.text
    if not age.isnumeric():
        await message.answer('Вводите только цифры!')
        return
    age = int(message.text)
    if age < 17:
        await message.answer('Для прохождения опроса вам должно быть минимум 17 лет')
        await state.clear()
    else:
        kb = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text='Мужской')],
                [types.KeyboardButton(text='Женский')]
            ],
            resize_keyboard=True
        )
        await state.update_data(age=age)
        await state.set_state(Survey.gender)
        await message.answer('Какого вы пола?', reply_markup=kb)


@survey_router.message(Survey.gender)
async def gender_handler(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text.capitalize())
    await state.set_state(Survey.occupation)
    kb = types.ReplyKeyboardRemove()
    await message.answer('Чем вы занимаетесь?', reply_markup=kb)


@survey_router.message(Survey.occupation)
async def name_handler(message: types.Message, state: FSMContext):
    await state.update_data(occupation=message.text)
    await message.answer('Спасибо за пройденный опрос!')
    data = await state.get_data()
    db.execute(query='''INSERT INTO survey_results(name, age, gender, occupation)
    VALUES (?, ?, ?, ?)''', params=(
        data.get('name'),
        data.get('age'),
        data.get('gender'),
        data.get('occupation')
    ))

    await state.clear()
