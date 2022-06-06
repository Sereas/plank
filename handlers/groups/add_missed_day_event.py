from aiogram.types import CallbackQuery

from loader import db


async def add_missed_day(call: CallbackQuery):
    print('callbackquerry: ', call.data.split(':')[-1].strip())
    person_missed = await db.check_if_user_exists(name=call.data.split(':')[-1].strip(),
                                                  chat_id=call.message.chat.id)
    total_debt = person_missed['total_debt']
    total_debt += person_missed['next_payment_amount']
    await db.update_parameter(parameter='total_debt',
                              new_value=total_debt,
                              user_id=person_missed['user_id'],
                              chat_id=person_missed['chat_id'])

    await db.update_parameter(parameter='next_payment_amount',
                              new_value=1000,
                              user_id=person_missed['user_id'],
                              chat_id=person_missed['chat_id'])
    await call.message.delete()
    await call.message.answer('Опа, новый пропуск! У ' + person_missed['name'] +
                              ' теперь долг в ' + str(total_debt) + ' рублей')
