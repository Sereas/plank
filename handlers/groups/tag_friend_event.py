import datetime

from aiogram.types import CallbackQuery

from handlers.groups.video_event import get_planked_date
from loader import db_logs, db


async def tag_friend(call: CallbackQuery):
    print('callbackquerry: ', call.data.split(':')[-1].strip())
    planked_date = await get_planked_date(call.message)
    you_planked = await db_logs.check_planked_today(user_id=call.from_user.id,
                                                    chat_id=call.message.chat.id,
                                                    check_date=planked_date)
    print('you planked: ', you_planked)
    if you_planked:
        friend = await db.check_if_user_exists(name=call.data.split(':')[-1].strip(),
                                               chat_id=call.message.chat.id)
        friend_planked = await db_logs.check_planked_today(id=friend['id'], check_date=planked_date)
        print('friend id:', friend['id'])
        print('friend planked: ', friend_planked)
        if friend_planked:
            await call.message.delete()
            await call.message.answer('А твой друг уже сегодня позанимался! Но ничего, лучше 2 раза, чем ни одного)')
        else:
            await db_logs.register_planked_today(id=friend['id'],
                                                 chat_id=friend['chat_id'],
                                                 user_id=friend['user_id'],
                                                 vacation=friend['vacation'],
                                                 planked=True,
                                                 check_date=planked_date)
            await call.message.delete()
            await call.message.answer('Отлично! Отметил, что ' + friend['name'] + ' позанимался сегодня, '
                                      + str(planked_date.strftime("%d/%m/%Y")))
    else:
        print('in false')
        await call.message.delete()
        await call.message.answer('Прости, но сначала я должен убедиться, что ты сам позанимался.')
