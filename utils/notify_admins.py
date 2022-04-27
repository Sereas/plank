import logging

from aiogram import Dispatcher

from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    admins = ADMINS
    try:
        print('admins', admins)
        for admin in admins:
            print('current admin', admin)
            await dp.bot.send_message(admin, "Бот Запущен")

    except Exception as err:
        logging.exception(err)
