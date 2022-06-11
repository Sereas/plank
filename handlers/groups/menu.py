from typing import Union

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, ParseMode
from aiogram.utils.markdown import markdown_decoration as markdown

from filters import AdminFilter
from handlers.groups.add_missed_day_event import add_missed_day
from handlers.groups.change_name_event import get_new_name
from handlers.groups.clear_misses_event import clear_misses
from handlers.groups.get_all_misses_event import show_all_misses
from handlers.groups.get_calendar_event import get_calendar
from handlers.groups.past_date_info_event import show_past_date_info
from handlers.groups.set_days_increase_event import get_days_increase
from handlers.groups.set_min_time_event import get_min_time
from handlers.groups.set_politeness_event import set_kind_politeness, set_rude_politeness
from handlers.groups.set_time_increase_event import get_time_increase
from handlers.groups.show_stats_event import show_my_stats
from handlers.groups.tag_friend_event import tag_friend
from handlers.groups.use_free_skip import use_free_skip
from handlers.groups.vacation_event import change_vacation_status
from keyboards.inline.buffs_keyboard import show_buffs_keyboard
from keyboards.inline.checkbox import names_tag_planked_checkbox, get_checked_users
from keyboards.inline.menu_keyboards import main_menu_keyboard, change_parameters_keyboard, menu_cd, \
    change_politeness_keyboard, names_tag_planked_keyboard, admin_cd, names_missed_day_keyboard
from loader import dp, db


@dp.message_handler(Command('menu'))
async def show_menu(message: Message):
    await list_categories(message)


async def list_categories(message: Union[Message, CallbackQuery], **kwargs):
    markup = await main_menu_keyboard()
    if isinstance(message, Message):
        await message.answer(markdown.pre('   --Меню бота:--   '), parse_mode=ParseMode.MARKDOWN_V2, reply_markup=markup)
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


async def politeness_change(callback: CallbackQuery):
    markup = await change_politeness_keyboard()
    await callback.message.edit_reply_markup(markup)


async def list_parameters(callback: CallbackQuery):
    markup = await change_parameters_keyboard()
    await callback.message.edit_reply_markup(markup)


async def names_to_tag(callback: CallbackQuery):
    markup = await names_tag_planked_checkbox(chat_id=callback.message.chat.id)
    await callback.message.edit_reply_markup(markup)


async def names_missed_day(callback: CallbackQuery):
    markup = await names_missed_day_keyboard(chat_id=callback.message.chat.id, callback=callback)
    await callback.message.edit_reply_markup(markup)

async def show_buffs(callback: CallbackQuery):
    await callback.message.delete()
    markup = await show_buffs_keyboard()
    await callback.message.answer(markdown.pre('   --Меню бота:--   '), parse_mode=ParseMode.MARKDOWN_V2, reply_markup=markup)



@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    print('callback data: ', callback_data)
    current_level = callback_data.get('level')
    levels = {
        "0": list_categories,
        "change_settings": list_parameters,
        "take_vacation": change_vacation_status,
        "set_min_time": get_min_time,
        "set_increase_time": get_time_increase,
        "set_days_increase": get_days_increase,
        "next_increase": get_calendar,
        "change_name": get_new_name,
        "change_politeness": politeness_change,
        "polite": set_kind_politeness,
        "rude": set_rude_politeness,
        "current_settings": show_my_stats,
        "tag_friend": names_to_tag,
        "name_chosen": tag_friend,
        "past_date_info": show_past_date_info,
        "show_all_misses": show_all_misses,
        "get_checked_users": get_checked_users,
        "show_buffs": show_buffs,
        "use_free_skip": use_free_skip,
    }
    current_level_function = levels[current_level]
    await current_level_function(call)


@dp.callback_query_handler(AdminFilter(), admin_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    print('callback data: ', callback_data)
    current_level = callback_data.get('level')
    levels = {
        "add_missed_day": names_missed_day,
        "name_chosen": add_missed_day,
        "clear_misses": names_missed_day,
        "name_chosen_clear_misses": clear_misses
    }
    current_level_function = levels[current_level]
    await current_level_function(call)
