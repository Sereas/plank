from aiogram.types import CallbackQuery

from loader import db


async def show_my_stats(callback: CallbackQuery):
    await callback.message.delete()
    user = await db.check_if_user_exists(id=str(str(callback.from_user.id)+str(callback.message.chat.id)),
                                         user_id=callback.from_user.id,
                                         chat_id=callback.message.chat.id,
                                         name=callback.from_user.first_name,
                                         full_name=callback.from_user.full_name)
    await callback.message.answer('Твоя текущая статистика: \n'
                                  'Имя: ' + user['name'] + '\n'
                                  'Текущее минимальное время: ' + str(user['current__time']) + ' секунд.\n'
                                  'Увеличение времени: ' + str(user['time_increase']) + ' секунд. \n'
                                  'Промежуток между увеличениями: ' + str(user['increase_in_days']) + ' дней.\n'
                                  'Дата следующего увеличения: ' + str(user['increase_day'].strftime("%d %b %Y") + '\n'
                                   'Режим отдыха: ' + str(user['vacation']) + '\n'
                                  'Количество пропусков: ' + str(user['times_missed']) + '\n'
                                  'Режим вежливости: ' + user['politeness'] + '\n'
                                  'Статус: ' + user['status']))

'''user = await db.check_if_user_exists(id=str(str(callback.from_user.id)+str(callback.message.chat.id)))'''