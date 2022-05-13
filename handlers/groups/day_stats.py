import datetime

import aiogram
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import ChatNotFound

from loader import db, db_logs, bot


async def get_day_stats(check_date=(datetime.datetime.today().date()-datetime.timedelta(days=1))):
    chats = await db.get_unique_values(column='chat_id')
    message_to_send = 'Дневная проверка активности за ' + str(check_date.strftime("%d %b %Y") + ':\n\n')
    for chat in chats:
        print('chat ', chat['chat_id'])
        users_in_chat = await db.select_all_rows_conditions(chat_id=chat['chat_id'])
        for user in users_in_chat:
            if user['vacation'] is False and user['status'] == 'active':
                planked = await db_logs.check_planked_today(id=user['id'], check_date=check_date)
                message_to_send += user['name'] + ' - ' + str(planked) + '\n'
        try:
            await bot.send_message(chat_id=chat['chat_id'], text=message_to_send)
        except ChatNotFound:
            print('Such chat does not exist anymore.')

