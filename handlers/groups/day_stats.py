import datetime

from aiogram.utils.exceptions import ChatNotFound, BotBlocked

from buffs.all_buffs import initialize_buff
from loader import db, db_logs, bot, db_buffs


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
        except BotBlocked:
            print('User ' + user['name'] + ' has blocked the bot.')
        message_to_send = 'Дневная проверка активности за ' + str(check_date.strftime("%d %b %Y") + ':\n\n')


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
                except BotBlocked:
                    print('User ' + user['name'] + ' has blocked the bot.')


async def eod_check_buffs_impact():
    print('checking buffs')
    eod_check_buffs = ['tough_guy', 'lucky_guy']
    all_active_buffs = await db_buffs.select_all_rows_conditions(table_name='Buffs', is_active=True)
    if len(all_active_buffs) == 0:
        print('Nobody has active buffs')
    else:
        for buff in all_active_buffs:
            buff_to_check = await initialize_buff(buff_code=buff['code'])
            await buff_to_check.load_existing_buff(id=buff['id'])
            if buff_to_check.code in eod_check_buffs:
                await buff_to_check.buff_action()
            else:
                print('This buff ' + buff_to_check.name + ' is not for eod check.')