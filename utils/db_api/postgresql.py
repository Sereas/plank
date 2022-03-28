import asyncio
import logging
from typing import Union
import datetime
from datetime import timedelta
import asyncpg
from asyncpg import Pool, Connection

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    '''async def create_connection(self):
        self.pool = await asyncpg.create_pool(
            user=config.USER,
            password=config.PASSWORD,
            host=config.HOST,
            port=config.PORT,
            database=config.DATABASE,
            max_inactive_connection_lifetime=5
        )'''

    async def execute(self, command, *args,
                      fetch: bool = False,  # достать массив массивов (много строк)
                      fetchval: bool = False,  # достать одно значение, например, кол-во пользователей
                      fetchrow: bool = False,  # достать одну строчку
                      execute: bool = False):
        logging.info('Создаем подключение к базе данных')
        self.pool = await asyncpg.create_pool(
            user=config.USER,
            password=config.PASSWORD,
            host=config.HOST,
            port=config.PORT,
            database=config.DATABASE,
            max_inactive_connection_lifetime=5
        )
        async with self.pool.acquire() as connection:
            connection: Connection
            logging.info('Idle connections before close: ' + str(self.pool.get_idle_size()))
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
        logging.info('Закрыаем подключения к базе данных')
        await self.pool.close()
        logging.info('Idle connections after close: ' + str(self.pool.get_idle_size()))
        return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS plank_schema.Users(
        id VARCHAR(255) NOT NULL UNIQUE,
        name VARCHAR(255) NOT NULL,
        full_name VARCHAR(255) NULL,
        chat_id BIGINT NOT NULL,
        user_id BIGINT NOT NULL,
        current__time INT NOT NULL,
        time_increase INT NOT NULL,
        increase_in_days INT NOT NULL,
        increase_day TIMESTAMP NOT NULL,
        date_joined TIMESTAMP NOT NULL,
        times_missed INT NOT NULL,
        planked_today BOOLEAN NOT NULL,
        vacation BOOLEAN NOT NULL,
        politeness VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    @staticmethod
    def format_args2(sql, parameters: dict):
        sql += "".join([
            f"{item}, " for item in parameters.keys()
        ])
        sql = sql[:-2] + ") VALUES("
        sql += "".join([
            f"${num}, " for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        sql = sql[:-2] + ") returning *"
        return sql, tuple(parameters.values())

    async def add_column(self):
        sql = """ALTER TABLE plank_schema.Users ADD COLUMN IF NOT EXISTS date_joined TIMESTAMP"""
        return await self.execute(sql, execute=True)

    '''To run code above and add new columns
    db = Database()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(db.add_column())'''

    async def add_user(self, **kwargs):
        sql = """INSERT INTO plank_schema.Users ("""
        static_params = {
            'current__time': 60,
            'time_increase': 10,
            'increase_in_days': 14,
            'increase_day': datetime.datetime.today().date() + timedelta(days=14),
            'date_joined': datetime.datetime.today().date(),
            'times_missed': 0,
            'planked_today': False,
            'vacation': False,
            'politeness': 'polite'
        }
        kwargs.update(static_params)
        sql, parameters = self.format_args2(sql, parameters=kwargs)
        return await self.execute(sql, *parameters,
                                  fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM plank_schema.Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM plank_schema.Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM plank_schema.Users"
        return await self.execute(sql, fetchval=True)

    async def update_name(self, name, user_id, chat_id):
        sql = "UPDATE plank_schema.Users SET name =$1 WHERE user_id=$2 AND chat_id=$3"
        return await self.execute(sql, name, user_id, chat_id, execute=True)

'''
db = Database()
loop = asyncio.get_event_loop()


loop.run_until_complete(db.create_connection())
loop.run_until_complete(db.create_table_users())


async def add_users():
    users = [
        ('1472583669', 'Olegg', 'DylevichOleg', 123, 456),
        ('9876546321', 'Kramm', 'Kram Kramovich', 123, 741),
        ('1234567689', 'Andreyy', 'Andrey Andreich', 123, 963)
    ]
    list_of_db_users = []
    for id, name, full_name, chat_id, user_id in users:
        user = await db.add_user(id=id, name=name, full_name=full_name, chat_id=chat_id, user_id=user_id)
        list_of_db_users.append(user)

loop.run_until_complete(add_users())
'''

