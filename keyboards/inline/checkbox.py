from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageToDeleteNotFound

from handlers.groups.get_all_users_name import get_names
from handlers.groups.video_event import get_planked_date
from keyboards.inline.menu_keyboards import make_callback_data
from loader import dp, db_logs, db

checkbox_cd = CallbackData('names_checkbox', 'name', 'is_checked')


def make_checkbox_callback_data(name, is_checked=False):
    return checkbox_cd.new(name=name, is_checked=is_checked)


def change_state_callback_data(name, is_checked):
    if is_checked:
        return checkbox_cd.new(name=name,  is_checked=False,)
    else:
        return checkbox_cd.new(name=name,  is_checked=True)


async def names_tag_planked_checkbox(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    print(chat_id)
    user_names = await get_names(chat_id=chat_id, status='active')
    callback_data, button_text = [],[]
    for user in user_names:
        callback_data.append(make_checkbox_callback_data(name=user))
        button_text.append(user)

    for button, callback in zip(button_text, callback_data):
        markup.insert(
            InlineKeyboardButton(text=button, callback_data=callback)
        )

    markup.row(
        InlineKeyboardButton(
            text='Отметить пользователей',
            callback_data=make_callback_data(level='get_checked_users')
        )
    )
    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level=0)
        )
    )
    return markup


@dp.callback_query_handler(checkbox_cd.filter())
async def process(call: CallbackQuery, callback_data: dict):
    markup = call.message.reply_markup
    new_markup = InlineKeyboardMarkup(row_width=2)
    name_to_change = callback_data.get('name')
    callback_data, button_text = [],[]
    old_markup = {}
    for row in markup.inline_keyboard:
        for button in row:
            if button.callback_data.split(':')[1].strip() != '0' and button.callback_data.split(':')[1].strip() != 'get_checked_users':
                if button.callback_data.split(':')[2].strip() == 'True':
                    status=True
                else:
                    status=False
                old_markup[button.callback_data.split(':')[1].strip()] = status

    for user in old_markup:
        if user != name_to_change:
            callback_data.append(make_checkbox_callback_data(name=user, is_checked=old_markup[user]))
            if old_markup[user]:
                button_text.append('✓ ' + user)
            else:
                button_text.append(user)
        else:
            callback_data.append(change_state_callback_data(name=user, is_checked=old_markup[user]))
            if old_markup[user]:
                button_text.append(user)
            else:
                button_text.append('✓ ' + user)

    for button, callback in zip(button_text, callback_data):
        new_markup.insert(
            InlineKeyboardButton(text=button, callback_data=callback)
        )

    new_markup.row(
        InlineKeyboardButton(
            text='Отметить пользователей',
            callback_data=make_callback_data(level='get_checked_users')
        )
    )

    new_markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level=0)
        )
    )
    await call.message.edit_reply_markup(new_markup)


async def get_checked_users(call: CallbackQuery):
    markup = call.message.reply_markup
    users_to_change = {}
    for row in markup.inline_keyboard:
        for button in row:
            if button.callback_data.split(':')[1].strip() != '0' and button.callback_data.split(':')[1].strip() != 'get_checked_users':
                if button.callback_data.split(':')[2].strip() == 'True':
                    status = True
                    users_to_change[button.callback_data.split(':')[1].strip()] = status
    print('users to change: ', users_to_change)
    print(len(users_to_change))
    if len(users_to_change) == 0:
        await call.message.delete()
        await call.message.answer('Надо выбрать хотя бы одного пользователя!')
    else:
        await tag_friend(call, users_to_change)


async def tag_friend(call: CallbackQuery, names):
    print('callbackquerry: ', call.data.split(':')[-1].strip())
    planked_date = await get_planked_date(call.message)
    you_planked = await db_logs.check_planked_today(user_id=call.from_user.id,
                                                    chat_id=call.message.chat.id,
                                                    check_date=planked_date)
    print('you planked: ', you_planked)
    if you_planked:
        for name in names:
            friend = await db.check_if_user_exists(name=name,
                                                   chat_id=call.message.chat.id)
            friend_planked = await db_logs.check_planked_today(id=friend['id'], check_date=planked_date)
            print('friend id:', friend['id'])
            print('friend planked: ', friend_planked)
            if friend_planked:
                try:
                    await call.message.delete()
                except MessageToDeleteNotFound:
                    pass
                await call.message.answer('А твой друг, ' +friend['name'] + ', уже сегодня позанимался! Но ничего, лучше 2 раза, чем ни одного)')
            else:
                await db_logs.register_planked_today(id=friend['id'],
                                                     chat_id=friend['chat_id'],
                                                     user_id=friend['user_id'],
                                                     vacation=friend['vacation'],
                                                     planked=True,
                                                     check_date=planked_date)
                try:
                    await call.message.delete()
                except MessageToDeleteNotFound:
                    pass

                await call.message.answer('Отлично! Отметил, что ' + friend['name'] + ' позанимался сегодня, '
                                          + str(planked_date.strftime("%d %b %Y")))
    else:
        print('in false')
        await call.message.delete()
        await call.message.answer('Прости, но сначала я должен убедиться, что ты сам позанимался.')



