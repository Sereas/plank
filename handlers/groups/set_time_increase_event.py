from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from loader import db, dp
from states import MenuStates


async def get_time_increase(callback: CallbackQuery):
    await callback.message.edit_text('А ты смелый! Или наоборот, трусишь)  \n'
                                     'Укажи новое увеличение времени в секундах:')
    await MenuStates.set_time_increase.set()


@dp.message_handler(state=MenuStates.set_time_increase)
async def set_time_increase(message: Message, state: FSMContext):
    answer = message.text
    try:
        int(answer)
        if isinstance(int(answer), int):
            user = await db.check_if_user_exists(message=message)
            await state.update_data(answer1=answer)
            await db.update_parameter(parameter='time_increase',
                                      new_value=int(answer),
                                      user_id=message.from_user.id,
                                      chat_id=message.chat.id)
            await message.answer(f'Ты ввел новое увеличение времени в размере  {answer} секунд, ' + user['name'])
            await state.finish()
    except ValueError:
        await message.answer('Надо ввести числовое значение, равное количеству секунд.')
        await MenuStates.set_time_increase.set()