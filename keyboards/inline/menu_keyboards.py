from aiogram.dispatcher.filters.state import State
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.groups.get_all_users_name import get_names

menu_cd = CallbackData('show_menu', 'level', 'name')
admin_cd = CallbackData('admin_function', 'level', 'name')


def make_callback_data(level, name='None'):
    return menu_cd.new(level=level, name=name)


def make_admin_callback_data(level, name='None'):
    return admin_cd.new(level=level, name=name)


async def main_menu_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=1)
    callback_data = [
        make_callback_data(level='tag_friend'),
        make_callback_data(level='current_settings'),
        make_callback_data(level='change_settings'),
        make_admin_callback_data(level='add_missed_day'),
        make_callback_data(level='past_date_info'),
        make_callback_data(level='show_all_misses'),
        make_admin_callback_data(level='clear_misses'),
        make_callback_data(level='show_buffs'),
        make_callback_data(level='use_free_skip')
    ]
    button_text = [
        'Отметить друга',  # level tag_friend
        'Мои текущие настройки',  # level current_settings
        'Изменить мои настройки',  # level change_settings
        'Добавить пропуск',  # level add_missed_day
        'Данные за прошлые даты',  # level past_date_info
        'Показать все пропуски',  # level show_all_misses
        'Убрать пропуски',  # level clear_misses
        'Использовать бафф',  # level show_buffs
        'Использовать день отдыха'  # level use_free_skip
    ]
    for button, callback in zip(button_text, callback_data):
        markup.insert(
            InlineKeyboardButton(text=button, callback_data=callback)
        )

    return markup


async def change_parameters_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_data = [
        make_callback_data(level='take_vacation'),
        make_callback_data(level='set_min_time'),
        make_callback_data(level='set_increase_time'),
        make_callback_data(level='set_days_increase'),
        make_callback_data(level='next_increase'),
        make_callback_data(level='change_name'),
        make_callback_data(level='change_politeness')
    ]
    button_text = [
        'Взять/прекрать перерыв',  # level take_vacation
        'Задать минимальное время',  # level set_min_time
        'Задать увеличение времени',  # level set_increase_time
        'Задать частоту увеличений',  # level set_days_increase
        'Задать дату следующего увеличения',  # level next_increase
        'Поменять имя',  # level change_name
        'Задать режим вежливости'  # level change_politeness
    ]
    for button, callback in zip(button_text, callback_data):
        markup.insert(
            InlineKeyboardButton(text=button, callback_data=callback)
        )
    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level=0)
        )
    )
    return markup


async def change_politeness_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_data = [
        make_callback_data(level='polite'),
        make_callback_data(level='rude')
    ]
    button_text = [
        'Будь со мной ласков',  # level polite
        'Я не против и грубо'  # level rude
    ]
    for button, callback in zip(button_text, callback_data):
        markup.insert(
            InlineKeyboardButton(text=button, callback_data=callback)
        )
    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level='change_settings')
        )
    )
    return markup


async def names_tag_planked_keyboard(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    user_names = await get_names(chat_id=chat_id, status='active')
    callback_data, button_text = [],[]
    for user in user_names:
        callback_data.append(make_callback_data(level='name_chosen', name=user))
        button_text.append(user)

    for button, callback in zip(button_text, callback_data):
        markup.insert(
            InlineKeyboardButton(text=button, callback_data=callback)
        )
    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level=0)
        )
    )
    return markup


async def names_missed_day_keyboard(chat_id, callback=None):
    markup = InlineKeyboardMarkup(row_width=2)
    user_names = await get_names(chat_id=chat_id)
    callback_data, button_text = [],[]
    if callback.data.split(':')[1].strip() == 'add_missed_day':
        for user in user_names:
            callback_data.append(make_admin_callback_data(level='name_chosen', name=user))
            button_text.append(user)
    elif callback.data.split(':')[1].strip() == 'clear_misses':
        for user in user_names:
            callback_data.append(make_admin_callback_data(level='name_chosen_clear_misses', name=user))
            button_text.append(user)

    for button, callback in zip(button_text, callback_data):
        markup.insert(
            InlineKeyboardButton(text=button, callback_data=callback)
        )
    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level=0)
        )
    )
    return markup
