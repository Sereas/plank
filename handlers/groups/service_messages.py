from aiogram import types
from loader import dp, db, bot
import asyncpg.exceptions


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):
    try:
        user = await db.add_user(
            id=str(str(message.new_chat_members[0].id)+str(message.chat.id)),
            name=message.new_chat_members[0].first_name,
            full_name=message.new_chat_members[0].full_name,
            chat_id=int(message.chat.id),
            user_id=int(message.new_chat_members[0].id))
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.add_user(
            id=str(str(message.new_chat_members[0].id)+str(message.chat.id)),
            name=str(message.new_chat_members[0].first_name) + str('New'),
            full_name=message.new_chat_members[0].full_name,
            chat_id=int(message.chat.id),
            user_id=int(message.new_chat_members[0].id))
    print('New user: ', user)

    members = ', '.join([m.get_mention() for m in message.new_chat_members])
    await bot.send_message(message.chat.id, 'Wazuuup, ' + members +'! I am very happy to see a new member in our cool and fun challenge!'
                                      ' I am pretty sure that whoever invited you has already explained all the simple rules '
                                      ' that we have to you. Nonetheless, I will give you a quick reminder of them ' + '\uE404 \n' +
                                      ' Rules: \n '
                                      ' 1. *Time limitation* Minimum participation time is 1 month'
                                      ' (No matter when you joined, check date is every 5th day of month). This day you'
                                      ' can decide whether to continue or to quit. If you quit early it is considered '
                                      ' as a defeat and leads to penalties. \n'
                                      ' 2. *Video* You are agreeing to do your exercise every day. The process has to be'
                                      ' filmed and sent to this chat. You have to say the date at the beginning of it.'
                                      ' The end of the day is considered to be the time you go to bed or 5am if you do'
                                      ' not. In rare circumstances it is acceptable not to send a video but "honestly"'
                                      ' tell the group that you have done your exercise(left your phone at home, it was'
                                      ' dead, etc... If you are on vacation with no access to Internet, you still have'
                                      ' to film yourself and send all videos when you return. \n'
                                      ' 3. *Skips* You may skip if you are ill (temp > 37.5) or injured. All other cases'
                                      ' have to be discussed individually and are considered as a defeat by default. \n'
                                      ' 4. *Difficulty* The challenge implies gradual increase in difficulty (at least'
                                      ' in the beginning). For example +5 sec every month. \n'
                                      ' 5. *Penalties* For each skipped day you have to pay 1000 rubles. We do not collect'
                                      ' more that 3000 rubles a month.')
    #message.reply