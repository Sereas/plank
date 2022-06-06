import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from buffs.all_buffs import get_all_buffs, initialize_buff
from keyboards.inline.buff_specific_buttons.LuckyGuyButtons import lucky_guy_buttons
from keyboards.inline.menu_keyboards import make_callback_data
from loader import dp, db_buffs

buff_cd = CallbackData('buff_function', 'level', 'name')


def make_buff_callback_data(level, name='None'):
    return buff_cd.new(level=level, name=name)


async def cancel_buff(buff_to_cancel, call):
    buff = await initialize_buff(buff_to_cancel)
    await buff.load_existing_buff(id=(str(call.from_user.id) + str(call.message.chat.id)))
    date_buff_cancelled = datetime.datetime.today().date()
    await buff.cancel(date_buff_ended=date_buff_cancelled, reason_buff_ended='user cancelled manually')
    await call.message.answer('Бафф "' + buff.name + '" отменен!')


async def process_buff(buff_to_process, call):
    has_buff = await db_buffs.select_row(table_name='Buffs',
                                         is_active=True,
                                         id=(str(call.from_user.id) + str(call.message.chat.id)))
    if has_buff is not None:
        await call.message.answer('У тебя уже активирован бафф ' + has_buff['name'] + '. Нельзя иметь больше одного активного баффа!')
    else:
        buff = await initialize_buff(buff_to_process)
        await buff.activate(id=str(call.from_user.id) + str(call.message.chat.id))
        await call.message.answer('Бафф '+ buff.name + ' активирован!')


async def get_description(buff_to_describe, call):
    buff = await initialize_buff(buff_to_describe)  # initialized empty buff
    description = await buff.describe()
    await buff.load_existing_buff((str(call.from_user.id) + str(call.message.chat.id)))
    if buff.is_active and buff_to_describe == buff.code:
        expired, days_left = await buff.is_expired()
        description += '\n' \
                       '\n' \
                       'У тебя уже активирован этот бафф и он будет действовать еще ' + str(days_left) + ' дней.'

    markup = await description_buff_keyboard(buff=buff, buff_to_describe=buff_to_describe)
    await call.message.answer(description, reply_markup=markup)


async def description_buff_keyboard(buff, buff_to_describe):
    markup = InlineKeyboardMarkup(row_width=1)
    if buff.is_active and buff_to_describe == buff.code:
        markup.insert(InlineKeyboardButton(
            text='Отменить бафф',
            callback_data=make_buff_callback_data(level='cancel_buff_' + buff.code)
        ))
        # Здесь будут создаваться специфичные кнопки для активного бафа (если они есть)
        if buff_to_describe == 'lucky_guy':
            buttons = await lucky_guy_buttons()
            for button in buttons:
                markup.insert(button)
    else:
        markup.insert(InlineKeyboardButton(
            text='Активировать',
            callback_data=make_buff_callback_data(level='process_buff_' + buff.code)
        ))

    markup.insert(InlineKeyboardButton(
            text=' Назад',
            callback_data=make_callback_data(level='show_buffs')
        ))

    return markup


async def show_buffs_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    all_buffs = await get_all_buffs()
    callback_data = []
    button_text = []
    for buff in all_buffs:
        callback_data.append(make_buff_callback_data(level='show_buff_' + buff))
        button_text.append(all_buffs[buff])

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


@dp.callback_query_handler(buff_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    await call.message.delete()
    current_level = callback_data.get('level')
    if 'show_buff' in current_level:
        await get_description(buff_to_describe=current_level[10:], call=call)
    if 'process_buff' in current_level:
        await process_buff(buff_to_process=current_level[13:], call=call)
    if 'cancel_buff' in current_level:
        await cancel_buff(buff_to_cancel=current_level[12:], call=call)
