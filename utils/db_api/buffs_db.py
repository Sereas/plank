from utils.db_api.parent_db import Database


class DatabaseBuffs(Database):
    async def create_table_buffs(self):
        sql = """
        CREATE TABLE IF NOT EXISTS plank_schema.Buffs(
        buff_id SERIAL,
        id VARCHAR(255) NOT NULL,
        code VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        date_buff_started TIMESTAMP NOT NULL,
        date_buff_ended TIMESTAMP,
        reason_buff_ended VARCHAR(255),
        is_active BOOLEAN NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_add_buff(sql, parameters: dict):
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

    async def add_buff(self, **kwargs):
        sql = """INSERT INTO plank_schema.Buffs ("""
        sql, parameters = self.format_add_buff(sql, parameters=kwargs)
        print('Adding buff')
        return await self.execute(sql, *parameters,
                                  execute=True)

    async def update_buff(self, parameter, new_value, id, buff_id):
        sql = "UPDATE plank_schema.Buffs SET " + parameter + " =$1 WHERE id=$2 AND buff_id=$3"
        return await self.execute(sql, new_value, id, buff_id, execute=True)
