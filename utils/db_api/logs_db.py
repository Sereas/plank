import datetime

from utils.db_api.parent_db import Database


class DatabaseLogs(Database):

    async def create_table_logs(self):
        sql = """
        CREATE TABLE IF NOT EXISTS plank_schema.Logs(
        id VARCHAR(255) NOT NULL,
        chat_id BIGINT NOT NULL,
        user_id BIGINT NOT NULL,
        check_date TIMESTAMP NOT NULL,
        planked BOOLEAN NOT NULL,
        vacation BOOLEAN NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args_planked_today(sql, parameters: dict):
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

    async def register_planked_today(self, message=None, **kwargs):
        if message:
            sql = """INSERT INTO plank_schema.Logs ("""
            static_params = {
                'id': str(message.from_user.id) + str(message.chat.id),
                'user_id': message.from_user.id,
                'chat_id': message.chat.id
            }
            kwargs.update(static_params)
            sql, parameters = self.format_args_planked_today(sql, parameters=kwargs)
            print('Adding log')
            return await self.execute(sql, *parameters,
                                      fetchrow=True)
        else:
            sql = """INSERT INTO plank_schema.Logs ("""
            sql, parameters = self.format_args_planked_today(sql, parameters=kwargs)
            print('Adding log')
            return await self.execute(sql, *parameters,
                                      fetchrow=True)

    async def check_planked_today(self, message=None, **kwargs):
        if message:
            user = await self.select_row(table_name='Logs',
                                         id= str(message.from_user.id) + str(message.chat.id),
                                         planked=True,
                                         **kwargs)
        else:
            user = await self.select_row(table_name='Logs',
                                         planked=True,
                                         **kwargs)
        if user is not None:
            return True
        else:
            return False




