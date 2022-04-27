from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from loader import db, dp
from states import MenuStates


async def get_days_increase(callback: CallbackQuery):
    await callback.message.edit_text('Тебя не устраивает частота изменений? Не беда! \n'
                                     'Укажи новую частоту в днях: ')
    await MenuStates.set_days_increase.set()


@dp.message_handler(state=MenuStates.set_days_increase)
async def set_days_increase(message: Message, state: FSMContext):
    answer = message.text
    try:
        int(answer)
        if isinstance(int(answer), int):
            user = await db.check_if_user_exists(message=message)
            await state.update_data(answer1=answer)
            await db.update_parameter(parameter='increase_in_days',
                                      new_value=int(answer),
                                      user_id=message.from_user.id,
                                      chat_id=message.chat.id)
            await message.answer(f'Ты ввел новую частоту изменения времи в размере  {answer} дней, ' + user['name'])
            await state.finish()
    except ValueError:
        await message.answer('Надо ввести числовое значение, равное количеству дней.')
        await MenuStates.set_days_increase.set()