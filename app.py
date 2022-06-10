import asyncio
import logging

from aiogram import executor

from handlers.groups.day_stats import get_day_stats, check_increases, eod_check_buffs_impact
from loader import dp, db, db_logs, scheduler, db_buffs
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


def set_scheduled_jobs(scheduler):
    # Добавляем задачи на выполнение
    scheduler.add_job(get_day_stats, "cron", day_of_week='mon-sun', hour=5, minute=0, timezone='Europe/Moscow')
    scheduler.add_job(eod_check_buffs_impact, "cron", day_of_week='mon-sun', hour=11, minute=53, timezone='Europe/Moscow')
    scheduler.add_job(eod_check_buffs_impact, "cron", day_of_week='mon-sun', hour=11, minute=25,
                      timezone='Europe/Moscow')
    scheduler.add_job(check_increases, "cron", day_of_week='mon-sun', hour=5, minute=10, timezone='Europe/Moscow')


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    logging.info('Запускаем таблицу пользователей')
    await db.create_table_users()
    await db_logs.create_table_logs()
    await db_buffs.create_table_buffs()
    logging.info('Готово')

    # Устанавливает команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    # запускает задачи по времени
    set_scheduled_jobs(scheduler)


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)




