
import datetime
from datetime import timedelta
import asyncpg

from utils.db_api.parent_db import Database


class DatabaseUsers(Database):

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
        total_debt INT NOT NULL,
        next_payment_amount INT NOT NULL,
        free_skips INT NOT NULL,
        vacation BOOLEAN NOT NULL,
        politeness VARCHAR(255) NOT NULL,
        status VARCHAR(255) NOT NULL,
        language VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args_add_user(sql, parameters: dict):
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

    async def add_user(self, **kwargs):
        try:
            sql = """INSERT INTO plank_schema.Users ("""
            static_params = {
                'current__time': 60,
                'time_increase': 10,
                'increase_in_days': 14,
                'increase_day': datetime.datetime.today().date() + timedelta(days=14),
                'date_joined': datetime.datetime.today().date(),
                'total_debt': 0,
                'next_payment_amount': 1000,
                'vacation': False,
                'free_skips': 0,
                'politeness': 'polite',
                'status': 'active',
                'language': 'ru'
            }
            kwargs.update(static_params)
            sql, parameters = self.format_args_add_user(sql, parameters=kwargs)
            print('Trying to add new user')
            return await self.execute(sql, *parameters,
                                      fetchrow=True)
        except asyncpg.exceptions.NotNullViolationError:
            print('Not enough data to create user')
        except asyncpg.exceptions.UniqueViolationError:
            print('duplicate key value violates unique constraint in table')
            user = await self.select_row(id=kwargs['id'])
            if user is None:
                print('adding new to name')
                kwargs['name'] = kwargs['name'] + 'New'
                print(kwargs['name'])
                await self.add_user(**kwargs)
            else:
                print('User ' + kwargs['name'] + ' already exists.')
                return user

    async def check_if_user_exists(self, message=None, **kwargs):
        print('Checking if user exists')
        if message is not None:
            user = await self.select_row(id=str(str(message.from_user.id) + str(message.chat.id)))
        else:
            user = await self.select_row(**kwargs)

        if user:
            print('User '+ user['name']+ ', exists')
            return user
        else:
            print('trying to add new user')
            if message is not None:
                await self.add_user(id=str(str(message.from_user.id)+str(message.chat.id)),
                                    user_id=message.from_user.id,
                                    chat_id=message.chat.id,
                                    name=message.from_user.first_name,
                                    full_name=message.from_user.full_name)
                user_new = await self.select_row(id=str(str(message.from_user.id) + str(message.chat.id)))
            else:
                user_new = await self.add_user(**kwargs)
            return user_new

    async def update_name(self, name, user_id, chat_id, table_name='Users'):
        sql = "UPDATE plank_schema.Users SET name =$1 WHERE user_id=$2 AND chat_id=$3"
        return await self.execute(sql, name, user_id, chat_id, execute=True)

'''
db = DatabaseUsers()
loop = asyncio.get_event_loop()

#loop.run_until_complete(db.create_connection())

loop.run_until_complete(db.create_table_users())
loop.run_until_complete(db.delete_row(chat_id=-645333939))

names = [149948231, 317396752, 479075524, 315906676, 217148052]
loop.run_until_complete(db.update_parameter(parameter='vacation', new_value=True, user_id=154642450, chat_id=-1001141146206))

async def add_users():
    users_db_path = '/Users/18356995/Downloads/users_db.h5'
    users_df = pd.read_hdf(users_db_path, key='df')
    list_of_users = users_df.values.tolist()
    print(users_df.values.tolist())
    users_to_add = []
    for user in list_of_users:
        user_to_add = (str(str(user[1]) + str(user[0])),
                       user[2],
                       user[2],
                       int(str(user[0])),
                       int(str(user[1])),
                       user[3],
                       user[4],
                       user[5],
                       user[6],
                       user[7])
        users_to_add.append(user_to_add)

    users = [
        ('1472581131669', 'Olegg', 'DylevichOleg', 123, 4561),
        ('9876546111321', 'Kramm', 'Kram Kramovich', 123, 7411),
        ('1234567111689', 'Andreyy', 'Andrey Andreich', 123, 9613)
    ]
    list_of_db_users = []
    for id, name, full_name, chat_id, user_id, current__time, time_increase, increase_in_days, increase_day, total_debt in users_to_add:
        user = await db.add_user(id=id,
                                 name=name,
                                 full_name=full_name,
                                 chat_id=chat_id,
                                 user_id=user_id,
                                 current__time=current__time,
                                 time_increase=time_increase,
                                 increase_in_days=increase_in_days,
                                 increase_day=increase_day,
                                 total_debt=total_debt)
        list_of_db_users.append(user)

loop.run_until_complete(add_users())
new_columns = {
    "test7": 'BIGINT'
}
#loop.run_until_complete(db.count_users())
#oleg = loop.run_until_complete(db.select_user(**{'name':'Olegg'}))
#andrey = loop.run_until_complete(db.select_user(name='Andrey23'))
#oleg = loop.run_until_complete(db.check_if_user_exists(name='Olegg', id='98345634741654', chat_id=687, user_id=11))
#print(oleg)
#loop.run_until_complete(db.update_parameter(parameter='name', new_value='Андрей', user_id=oleg['user_id'], chat_id=oleg['chat_id']))
'''
