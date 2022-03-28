from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Буся'),
            KeyboardButton(text='Пумпуся')
        ]
    ],
    resize_keyboard=True
)