from typing import Union

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from handlers.groups.get_calendar_event import get_calendar
from handlers.groups.set_days_increase_event import get_days_increase
from handlers.groups.set_min_time_event import get_min_time
from handlers.groups.set_time_increase_event import get_time_increase
from handlers.groups.show_stats_event import show_my_stats
from handlers.groups.vacation_event import change_vacation_status
from keyboards.inline.menu_keyboards import main_menu_keyboard, change_parameters_keyboard, menu_cd
from loader import dp, db


@dp.message_handler(Command('menu'))
async def show_menu(message: Message):
    await list_categories(message)


async def list_categories(message: Union[Message, CallbackQuery], **kwargs):
    markup = await main_menu_keyboard()
    if isinstance(message, Message):
        await message.answer('Меню бота: ', reply_markup=markup)
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


async def list_parameters(callback: CallbackQuery):
    markup = await change_parameters_keyboard()
    await callback.message.edit_reply_markup(markup)


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    current_level = callback_data.get('level')
    levels = {
        "0": list_categories,
        "1": list_parameters,
        "2": change_vacation_status,
        "3": get_min_time,
        "4": get_time_increase,
        "5": get_days_increase,
        "6": get_calendar,
        "30": show_my_stats
    }
    current_level_function = levels[current_level]
    await current_level_function(call)

