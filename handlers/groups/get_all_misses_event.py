from aiogram.types import CallbackQuery

from loader import db


async def show_all_misses(callback: CallbackQuery):
    await callback.message.delete()
    users = await db.select_all_rows_conditions(chat_id=callback.message.chat.id)
    message = 'Вот список текущих должников: \n'
    for user in users:
        if user['times_missed'] > 0:
            message += user['name'] + ' - ' + str(user['times_missed']) + '\n'
    await callback.message.answer(message)
