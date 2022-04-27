from aiogram.types import CallbackQuery

from loader import db


async def change_vacation_status(callback: CallbackQuery):
    await callback.message.delete()
    user = await db.check_if_user_exists(id=str(str(callback.from_user.id) + str(callback.message.chat.id)))
    if user['vacation']:
        await callback.message.answer('Ура! Мы рады твоему возвращению, ' + user['name'])
        await db.update_parameter(parameter='vacation',
                                  new_value=False,
                                  user_id=callback.from_user.id,
                                  chat_id=callback.message.chat.id)
    else:
        await callback.message.answer('О нет, надеюсь с тобой все в порядке и ты скоро будешь в строю, ' + user['name'])
        await db.update_parameter(parameter='vacation',
                                  new_value=True,
                                  user_id=callback.from_user.id,
                                  chat_id=callback.message.chat.id)