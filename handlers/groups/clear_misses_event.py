from aiogram.types import CallbackQuery

from loader import db


async def clear_misses(call: CallbackQuery):
    print('callbackquerry: ', call.data.split(':')[-1].strip())
    person_to_clear = await db.check_if_user_exists(name=call.data.split(':')[-1].strip(),
                                                  chat_id=call.message.chat.id)
    await db.update_parameter(parameter='total_debt',
                              new_value=0,
                              user_id=person_to_clear['user_id'],
                              chat_id=person_to_clear['chat_id'])
    await call.message.delete()
    await call.message.answer('Ура, ' + person_to_clear['name'] +
                              ', заплатил! Теперь все будет с чистого листа! ')