from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, Message
from datetime import datetime

from handlers.groups.day_stats import get_day_stats
from loader import dp, db
from states import MenuStates
from aiogram_calendar import simple_cal_callback, SimpleCalendar


async def get_calendar(callback: Union[CallbackQuery, Message]):
    print('callbackquerry: ', callback.data.split(':')[1].strip())
    if callback.data.split(':')[1].strip() == 'next_increase':
        if isinstance(callback, Message):
            await callback.answer('Выбери дату: ',
                                  reply_markup=await SimpleCalendar().start_calendar())
        elif isinstance(callback, CallbackQuery):
            await callback.message.edit_text('Выбери дату: ',
                                             reply_markup=await SimpleCalendar().start_calendar())
        await MenuStates.get_calendar_date.set()
    elif callback.data.split(':')[1].strip() == 'past_date_info':
        if isinstance(callback, Message):
            await callback.answer('Выбери дату: ',
                                  reply_markup=await SimpleCalendar().start_calendar())
        elif isinstance(callback, CallbackQuery):
            await callback.message.edit_text('Выбери дату: ',
                                             reply_markup=await SimpleCalendar().start_calendar())
        await MenuStates.previous_date_stat.set()


# simple calendar usage
@dp.callback_query_handler(simple_cal_callback.filter(),
                           state=MenuStates.get_calendar_date)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    today = datetime.today()
    if selected:
        if date > today:
            await db.update_parameter(parameter='increase_day',
                                      new_value=date,
                                      user_id=callback_query.from_user.id,
                                      chat_id=callback_query.message.chat.id)
            await callback_query.message.answer(
                f'Ты выбрал {date.strftime("%d %b %Y")}',
                reply_markup=ReplyKeyboardRemove()
            )
            await state.finish()
        else:
            reply = await callback_query.message.answer('Дата должна быть больше, чем сегодня.')
            await state.finish()
            await get_calendar(reply)


@dp.callback_query_handler(simple_cal_callback.filter(),
                           state=MenuStates.previous_date_stat)
async def process_simple_calendar2(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    await get_day_stats(check_date=date)
    await state.finish()

