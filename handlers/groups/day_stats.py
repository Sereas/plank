import datetime

from aiogram.utils.exceptions import ChatNotFound

from loader import db, db_logs, bot


async def get_day_stats(check_date=None):
    if check_date is None:
        check_date = (datetime.datetime.today() - datetime.timedelta(days=1))
    chats = await db.get_unique_values(column='chat_id')
    message_to_send = 'Дневная проверка активности за ' + str(check_date.strftime("%d %b %Y") + ':\n\n')
    for chat in chats:
        print('chat ', chat['chat_id'])
        users_in_chat = await db.select_all_rows_conditions(chat_id=chat['chat_id'])
        users_in_logs = await db_logs.select_all_rows_conditions(table_name='Logs', chat_id=chat['chat_id'], check_date=check_date.date())
        for user in users_in_chat:
            if user['vacation'] is False and user['status'] == 'active' and user['date_joined'].date() <= check_date.date():
                if not any(dictionary['id'] == user['id'] for dictionary in users_in_logs):
                    message_to_send += user['name'] + ' - False \n'
                else:
                    message_to_send += user['name'] + ' - True \n'
        try:
            await bot.send_message(chat_id=chat['chat_id'], text=message_to_send)
        except ChatNotFound:
            print('Such chat does not exist anymore.')


async def check_increases():
    print('checking increases')
    chats = await db.get_unique_values(column='chat_id')
    today = datetime.datetime.today().date()
    for chat in chats:
        users_in_chat = await db.select_all_rows_conditions(chat_id=chat['chat_id'])
        for user in users_in_chat:
            if user['status'] == 'active' and today >= user['increase_day'].date():
                new_time = user['current__time'] + user['time_increase']
                new_increase_day = user['increase_day'] + datetime.timedelta(days=int(user['increase_in_days']))
                await db.update_parameter(parameter='current__time',
                                          new_value=new_time,
                                          user_id=user['user_id'],
                                          chat_id=user['chat_id'])
                await db.update_parameter(parameter='increase_day',
                                          new_value=new_increase_day,
                                          user_id=user['user_id'],
                                          chat_id=user['chat_id'])
                message_to_send = 'У ' + user['name'] + ' сегодня изменение времени! Новое время - ' \
                                  + str(new_time) + ' секунд. \n' \
                                                    'Следующее увеличение ' + str(new_increase_day.strftime("%d %b %Y"))
                try:
                    await bot.send_message(chat_id=chat['chat_id'], text=message_to_send)
                except ChatNotFound:
                    print('Such chat does not exist anymore.')
