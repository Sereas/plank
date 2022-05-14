from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import logging

from data import config
from utils.db_api.users_db import DatabaseUsers
from utils.db_api.logs_db import DatabaseLogs
from apscheduler.schedulers.asyncio import AsyncIOScheduler

loop = asyncio.get_event_loop()
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                    )

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DatabaseUsers()
db_logs = DatabaseLogs()
scheduler = AsyncIOScheduler()
