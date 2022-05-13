from aiogram.types import CallbackQuery

from loader import db


async def add_missed_day(call: CallbackQuery):
    print('callbackquerry: ', call.data.split(':')[-1].strip())
    person_missed = await db.check_if_user_exists(name=call.data.split(':')[-1].strip(),
                                                  chat_id=call.message.chat.id)
    times_missed = person_missed['times_missed']
    times_missed += 1
    await db.update_parameter(parameter='times_missed',
                              new_value=times_missed,
                              user_id=person_missed['user_id'],
                              chat_id=person_missed['chat_id'])
    await call.message.delete()
    await call.message.answer('Опа, новый пропуск! У ' + person_missed['name'] +
                              ' теперь ' + str(times_missed) + ' пропусков')
