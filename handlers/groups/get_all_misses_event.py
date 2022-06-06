from aiogram.types import CallbackQuery

from loader import db, storage


async def show_all_misses(callback: CallbackQuery):
    await callback.message.delete()
    users = await db.select_all_rows_conditions(chat_id=callback.message.chat.id)
    message = 'Вот список текущих должников: \n'
    for user in users:
        if user['total_debt'] > 0:
            message += user['name'] + ' - ' + str(user['total_debt']) + ' рублей. \n'
    await callback.message.answer(message)
