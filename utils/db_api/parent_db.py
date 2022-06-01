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

    @staticmethod
    def format_args_multiple_conditions(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def select_all_rows_conditions(self, table_name='Users', **kwargs):
        sql = "SELECT * FROM plank_schema." + table_name + " WHERE "
        sql, parameters = self.format_args_multiple_conditions(sql, parameters=kwargs)
        print(sql)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_row(self, table_name='Users', **kwargs):
        sql = "SELECT * FROM plank_schema." + table_name + " WHERE "
        sql, parameters = self.format_args_multiple_conditions(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self, table_name='Users'):
        sql = "SELECT COUNT(*) FROM plank_schema." + table_name
        return await self.execute(sql, fetchval=True)

    async def update_parameter(self, parameter, new_value, user_id, chat_id, table_name='Users'):
        sql = "UPDATE plank_schema." + table_name + " SET " + parameter + " =$1 WHERE user_id=$2 AND chat_id=$3"
        print(sql)
        return await self.execute(sql, new_value, user_id, chat_id, execute=True)

    async def add_column(self, new_columns, table_name='Users'):
        sql = """ALTER TABLE plank_schema.""" + table_name
        for key, value in new_columns.items():
            sql += " ADD COLUMN IF NOT EXISTS " + key + ' ' + value + ","
        sql = sql[:-1]
        return await self.execute(sql, execute=True)

    '''To run code above and add new columns
    db = Database()
    loop = asyncio.get_event_loop()
    new_columns = {
        "test1": 'BIGINT',
        "test2": 'BIGINT'
    }
    loop.run_until_complete(db.add_column(new_columns))'''

    async def get_unique_values(self, column, table_name='Users'):
        sql = "SELECT DISTINCT " + column + " FROM plank_schema." + table_name
        return await self.execute(sql, fetch=True)

    async def delete_row(self, table_name='Users', **kwargs):
        sql = "DELETE FROM plank_schema." + table_name + " WHERE "
        sql, parameters = self.format_args_multiple_conditions(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, execute=True)

    async def delete_column(self, column, table_name='Users'):
        sql = "ALTER TABLE plank_schema." + table_name + " DROP COLUMN " + column
        return await self.execute(sql, execute=True)