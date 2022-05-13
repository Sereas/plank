import asyncio
import logging

from aiogram import executor

from loader import dp, db, db_logs
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    logging.info('Запускаем таблицу пользователей')
    await db.create_table_users()
    await db_logs.create_table_logs()
    logging.info('Готово')

    # Устанавливает команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)




