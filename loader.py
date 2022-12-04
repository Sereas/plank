from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import logging

from data import config
from utils.db_api.buffs_db import DatabaseBuffs
from utils.db_api.users_db import DatabaseUsers
from utils.db_api.logs_db import DatabaseLogs
from apscheduler.schedulers.asyncio import AsyncIOScheduler

loop = asyncio.get_event_loop()

file_handler = logging.FileHandler("All_logs.log")
file_handler.setLevel(logging.WARNING)
stream_handler = logging.StreamHandler()
logging.basicConfig(format=f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
                    level=logging.INFO,
                    handlers=(file_handler, stream_handler),
                    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                    )

_log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DatabaseUsers()
db_logs = DatabaseLogs()
db_buffs = DatabaseBuffs()
scheduler = AsyncIOScheduler()
