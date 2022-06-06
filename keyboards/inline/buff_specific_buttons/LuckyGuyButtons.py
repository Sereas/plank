from aiogram.types import InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from buffs.all_buffs import initialize_buff
from loader import dp

lucky_guy_cd = CallbackData('lucky_guy_buff_buttons', 'level')


def make_lucky_guy_buff_callback_data(level):
    return lucky_guy_cd.new(level=level)


async def get_today_delta(callback: CallbackQuery):
    lucky_guy_buff = await initialize_buff(buff_code='lucky_guy')
    await lucky_guy_buff.load_existing_buff(id=(str(callback.from_user.id) + str(callback.message.chat.id)))
    today_delta = await lucky_guy_buff.today_time()
    if today_delta <= 40:
        roll_god_attitude = 'благосклоны'
    else:
        roll_god_attitude = 'не благосклоны'

    markup = await lucky_guy_yes_no_keyboard()
    await callback.message.answer('Боги ролла к тебе сегодня ' + roll_god_attitude + '! \n'
                                     'Они предлагают тебе увеличить время на ' + str(today_delta) + '%\n'
                                      'Согласен?',
                                  reply_markup=markup)

async def lucky_guy_buttons():
    buttons = []
    get_today_delta = InlineKeyboardButton(
        text='Изменение времени на сегодня',
        callback_data=make_lucky_guy_buff_callback_data(level='get_today_delta' )
    )
    buttons.append(get_today_delta)
    return buttons

async def lucky_guy_yes_no_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)

    markup.insert(InlineKeyboardButton(
        text='Да',
        callback_data=make_lucky_guy_buff_callback_data(level='yes')
    ))
    markup.insert(InlineKeyboardButton(
        text='Нет',
        callback_data=make_lucky_guy_buff_callback_data(level='no')
    ))

    return markup


@dp.callback_query_handler(lucky_guy_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    await call.message.delete()
    current_level = callback_data.get('level')
    if 'get_today_delta' in current_level:
        await get_today_delta(call)

