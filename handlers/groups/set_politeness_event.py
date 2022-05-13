from aiogram.types import CallbackQuery
from loader import db


async def set_kind_politeness(callback: CallbackQuery):
    await callback.message.delete()
    user = await db.check_if_user_exists(id=str(str(callback.from_user.id) + str(callback.message.chat.id)))
    await db.update_parameter(parameter='politeness',
                              new_value='polite',
                              user_id=callback.from_user.id,
                              chat_id=callback.message.chat.id)
    await callback.message.answer('Готово, мой любимый котенок ' + user['name'])


async def set_rude_politeness(callback: CallbackQuery):
    await callback.message.delete()
    user = await db.check_if_user_exists(id=str(str(callback.from_user.id) + str(callback.message.chat.id)))
    await db.update_parameter(parameter='politeness',
                              new_value='rude',
                              user_id=callback.from_user.id,
                              chat_id=callback.message.chat.id)
    await callback.message.answer('О, да, ' + user['name'] + '! Мы с тобой повеселимся!')
