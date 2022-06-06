from typing import Union
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery


class AdminFilter(BoundFilter):
    async def check(self, message: Union[Message, CallbackQuery]) -> bool:
        print('in admin filter')
        if isinstance(message, Message):
            member = await message.chat.get_member(message.from_user.id)
            if member.is_chat_admin() is False:
                await message.answer('Этой функцией может пользоваться только администратор.')
        elif isinstance(message, CallbackQuery):
            member = await message.message.chat.get_member(message.from_user.id)
            if member.is_chat_admin() is False:
                await message.message.answer('Этой функцией может пользоваться только администратор.')
        return member.is_chat_admin()