from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from loader import db, dp
from states import MenuStates


async def get_new_name(callback: CallbackQuery):
    await callback.message.edit_text('Мне тоже кажется, что тебе не идет это имя =) Как будем тебя теперь звать?')
    await MenuStates.set_new_name.set()


@dp.message_handler(state=MenuStates.set_new_name)
async def set_new_name(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)
    await db.update_parameter(parameter='name',
                              new_value=answer,
                              user_id=message.from_user.id,
                              chat_id=message.chat.id)
    await message.answer(f'Отныне и вовеки веков, мы будем звать тебя {answer} ')
    await state.finish()
