from aiogram.types import InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup, Dice
from aiogram.utils.callback_data import CallbackData

from buffs.all_buffs import initialize_buff
from loader import dp, db, storage, bot

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
    dice = await callback.message.answer_dice()
    print('Dice roll: ', dice.dice.value)
    await callback.message.answer('Боги ролла к тебе сегодня ' + roll_god_attitude + '! \n'
                                     'Они предлагают тебе увеличить время на ' + str(today_delta) + '%\n'
                                      'Согласен?',
                                  reply_markup=markup)


async def lucky_guy_refused(callback: CallbackQuery):
    lucky_guy_buff = await initialize_buff(buff_code='lucky_guy')
    await lucky_guy_buff.load_existing_buff(id=(str(callback.from_user.id) + str(callback.message.chat.id)))
    user = await db.check_if_user_exists(id=lucky_guy_buff.id)
    await callback.message.answer('Ну ты даешь, ' + user['name'] + ', я немного расстроен( \n'
                                  'Время осталось прежним: ' + str(user['current__time']) + 'секунд, а вот платеж увеличится'
                                  ' на ' + str(lucky_guy_buff.money_delta) + ' рублей.' )
    await lucky_guy_buff.set_state_accepted(data=False)


async def lucky_guy_agreed(callback: CallbackQuery):
    lucky_guy_buff = await initialize_buff(buff_code='lucky_guy')
    await lucky_guy_buff.load_existing_buff(id=(str(callback.from_user.id) + str(callback.message.chat.id)))
    await lucky_guy_buff.set_state_base_time()
    await lucky_guy_buff.set_state_accepted(data=True)

    user = await db.check_if_user_exists(id=lucky_guy_buff.id)
    rolled_time = (await storage.get_data(chat=user['chat_id'], user=(str(user['user_id']) + '_today_time')))/100
    today_time = int((1+rolled_time) * user['current__time'])

    await db.update_parameter(parameter='current__time',
                              new_value=today_time,
                              user_id=user['user_id'],
                              chat_id=user['chat_id'])

    new_payment = user['next_payment_amount'] - lucky_guy_buff.money_delta
    await callback.message.answer('Поражаюсь твоей смелости, ' + user['name'] + '! Сегодня тебе нужно будет отстоять '
                                  + str(today_time) + ' секунд, но зато твой следующий платеж будет всего ' + str(new_payment) + ' рублей.')


async def lucky_guy_buttons():
    buttons = []
    get_today_delta_button = InlineKeyboardButton(
        text='Изменение времени на сегодня',
        callback_data=make_lucky_guy_buff_callback_data(level='get_today_delta' )
    )
    buttons.append(get_today_delta_button)
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
    elif 'yes' in current_level:
        print('you agreed to increase time')
        await lucky_guy_agreed(call)
    elif 'no' in current_level:
        print('you refused to increase time')
        await lucky_guy_refused(call)

