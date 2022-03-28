from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.default import menu
from loader import dp


@dp.message_handler(Command('menu'))
async def show_menu(message: Message):
    await message.answer('Викуся кто?', reply_markup=menu)


@dp.message_handler(Text(equals=['Буся', 'Пумпуся']))
async def get_Vika(message: Message):
    await message.answer(f'Вы выбрали {message.text}. Хороший выбор!', reply_markup=ReplyKeyboardRemove())
    if message.text == 'Буся':
        await message.answer('Я тоже так считаю.')
    elif message.text == 'Пумпуся':
        await message.answer('Но я считаю по другому.')
