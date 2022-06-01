from typing import Union
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery

from loader import db_buffs, storage



class ToughGuyFilter(BoundFilter):
    async def check(self, message: Union[Message, CallbackQuery]) -> bool:
        if isinstance(message, Message):
            await storage.reset_state(user=message.from_user.id, chat=message.chat.id)
            is_buff = await db_buffs.select_row(table_name='Buffs',
                                          id=(str(message.from_user.id) + str(message.chat.id)),
                                          is_active=True)
            if is_buff is None:
                passed = True
            else:
                if is_buff['code'] == 'tough_guy':
                    passed = False
                    await message.answer('У тебя активирован бафф, менять время нельзя.')
                else:
                    passed = True

        elif isinstance(message, CallbackQuery):
            await storage.reset_state(user=message.from_user.id, chat=message.message.chat.id)
            is_buff = await db_buffs.select_row(table_name='Buffs',
                                            id=(str(message.from_user.id) + str(message.message.chat.id)),
                                            is_active=True)
            if is_buff is None:
                passed = True
            else:
                if is_buff['code'] == 'tough_guy':
                    passed = False
                    await message.message.answer('У тебя активирован бафф, менять время нельзя.')
                else:
                    passed = True
        return passed


