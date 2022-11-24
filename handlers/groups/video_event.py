import datetime

from aiogram import types
from aiogram.types import Message

from loader import dp, db, db_logs


@dp.message_handler(content_types=types.ContentType.VIDEO)
async def receive_video(message: Message):
    user = await db.check_if_user_exists(message=message)
    user_min_time = user['current__time']
    video_length = message.video.duration
    planked_date = await get_planked_date(message)
    needed_length = await check_length(user_min_time=user_min_time, video_length=video_length)
    check_planked_today = await db_logs.check_planked_today(message=message, check_date=planked_date)
    if check_planked_today:
        await message.answer('Дружок, ты сегодня уже занимался =)')
    else:
        if needed_length is False:
            await message.answer('Прости, но кто-то не выполнил свою дневную норму( \n'
                                 'Тебе необходимо заниматься минимум ' + str(user_min_time) + ' секунд. \n'
                                 'Твое видео длиной всего ' + str(video_length) + '.')
        else:
            await db_logs.register_planked_today(message=message,
                                                 check_date=planked_date,
                                                 planked=True,
                                                 vacation=user['vacation'])
            await message.answer('Ура! Поздравляю с очередным продуктивным днем, ' +
                                 message.from_user.get_mention() + ', ' + str(planked_date.strftime("%d %b %Y")))


async def check_length(user_min_time, video_length):
    if video_length < user_min_time:
        return False
    else:
        return True


async def get_planked_date(message: Message):
    time_sent = message.date.utcnow()
    if time_sent.hour < 2:
        planked_date = datetime.datetime.today() - datetime.timedelta(days=1)
    else:
        planked_date = datetime.datetime.today()
    return planked_date.date()




