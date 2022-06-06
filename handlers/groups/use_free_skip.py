import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from aiogram.utils import markdown
from aiogram.utils.callback_data import CallbackData


from keyboards.inline.menu_keyboards import make_callback_data, main_menu_keyboard
from loader import db, dp, db_logs, storage
from states import MenuStates

free_skip_cd = CallbackData('free_skip', 'level')


def make_free_skip_callback_data(level):
    return free_skip_cd.new(level=level)


async def free_skip_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(
            text='Использовать',
            callback_data=make_free_skip_callback_data(level='use_free_skip')
        ))

    markup.insert(InlineKeyboardButton(
            text=' Назад',
            callback_data=make_free_skip_callback_data(level='go_back')
        ))

    return markup


async def use_free_skip(call: CallbackQuery):
    user = await db.check_if_user_exists(id=(str(call.from_user.id) + str(call.message.chat.id)))
    if user['free_skips'] is not None and user['free_skips'] > 0:
        await MenuStates.free_skip.set()
        await call.message.edit_text('Хочешь использовать день отдыха? Чтож, ты заслужил, у тебя их целых ' + str(user['free_skips']))
        markup = await free_skip_keyboard()
        await call.message.edit_reply_markup(reply_markup=markup)
    else:
        await call.message.delete()
        await call.message.answer('Прости, но я не вижу у тебя накопленые дни отдыха. Попробуй воспользоваться бафами.')


@dp.callback_query_handler(free_skip_cd.filter(), state=MenuStates.free_skip)
async def navigate(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    current_level = callback_data.get('level')
    if 'use_free_skip' in current_level:
        print('in free skip')
        await state.finish()
        planked_date = datetime.datetime.today().date()
        user = await db.check_if_user_exists(id=(str(call.from_user.id) + str(call.message.chat.id)))
        await db.update_parameter(parameter='free_skips',
                                  new_value=int(user['free_skips'] - 1),
                                  user_id=user['user_id'],
                                  chat_id=user['chat_id'])

        await db_logs.register_planked_today(id=user['id'],
                                             chat_id=user['chat_id'],
                                             user_id=user['user_id'],
                                             check_date=planked_date,
                                             planked=True,
                                             vacation=user['vacation'])

        await call.message.answer('Готово, ' + user['name'] + ', можешь сегодня отдохнуть, ' + str(planked_date.strftime("%d %b %Y")))

    elif 'go_back' in current_level:
        await state.finish()
        markup = await main_menu_keyboard()
        await call.message.answer(markdown.pre('   --Меню бота:--   '), parse_mode=ParseMode.MARKDOWN_V2,reply_markup=markup)


@dp.callback_query_handler(free_skip_cd.filter())
async def test(call: CallbackQuery, callback_data: dict):
    await call.message.answer('Прости, ' + call.from_user.first_name + ', но это не ты захотел использовать день отдыха.')