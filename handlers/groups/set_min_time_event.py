from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from loader import db, dp
from states import MenuStates


async def get_min_time(callback: CallbackQuery):
    await callback.message.edit_text('Кто-то решил поменять время? Хорошо. я уверен, что новое время '
                                     'принесет тебе больше удовольствия! \n'
                                     'Укажи новое время в секундах:')
    await MenuStates.set_min_time.set()


@dp.message_handler(state=MenuStates.set_min_time)
async def set_min_time(message: Message, state: FSMContext):
    answer = message.text
    try:
        int(answer)
        if isinstance(int(answer), int):
            user = await db.check_if_user_exists(message=message)
            await state.update_data(answer1=answer)
            await db.update_parameter(parameter='current__time',
                                      new_value=int(answer),
                                      user_id=message.from_user.id,
                                      chat_id=message.chat.id)
            await message.answer(f'Ты ввел новое время в размере  {answer} секунд, ' + user['name'])
            await state.finish()
    except ValueError:
        await message.answer('Надо ввести числовое значение, равное количеству секунд.')
        await MenuStates.set_min_time.set()