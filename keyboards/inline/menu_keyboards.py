from aiogram.dispatcher.filters.state import State
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_cd = CallbackData('show_menu', 'level')


def make_callback_data(level):
    return menu_cd.new(level=level)


async def main_menu_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=1)
    callback_data = [
        make_callback_data(level=20),
        make_callback_data(level=30),
        make_callback_data(level=1),
        make_callback_data(level=40),
        make_callback_data(level=50),
        make_callback_data(level=60),
        make_callback_data(level=70)
        ]
    button_text = [
        'Сделал упражнение с другом',  # level 20
        'Мои текущие настройки',  # level 30
        'Изменить мои настройки',  # level 1
        'Добавить пропуск',  # level 40
        'Данные за прошлые даты',  # level 50
        'Показать все пропуски',  # level 60
        'Убрать пропуски'  # level 70
    ]
    for button, callback in zip(button_text, callback_data):
        markup.insert(
            InlineKeyboardButton(text=button, callback_data=callback)
        )

    return markup


async def change_parameters_keyboard():
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)
    callback_data = [
        make_callback_data(level=2),
        make_callback_data(level=3),
        make_callback_data(level=4),
        make_callback_data(level=5),
        make_callback_data(level=6),
        make_callback_data(level=7),
        make_callback_data(level=8)
        ]
    button_text = [
        'Взять перерыв',  # level 2
        'Задать минимальное время',  # level 3
        'Задать увеличение времени',  # level 4
        'Задать частоту увеличений',  # level 5
        'Задать дату следующего увеличения',  # level 6
        'Переименовать пользователя',  # level 7
        'Задать режим вежливости'  # level 8
    ]
    for button, callback in zip(button_text, callback_data):
        markup.insert(
            InlineKeyboardButton(text=button, callback_data=callback)
        )
    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level=CURRENT_LEVEL-1)
        )
    )
    return markup
