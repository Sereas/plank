import psycopg2
from psycopg2 import Error
from data import config
global connection, cursor

SQLquerry = 'CREATE TABLE hof_main.supplies (id INT PRIMARY KEY, name VARCHAR, description VARCHAR, manufacturer VARCHAR, color VARCHAR, inventory int CHECK (inventory > 0));'

def connect_to_db():
    global connection, cursor
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=config.USER,
                                      password=config.PASSWORD,
                                      host=config.HOST,
                                      port=config.PORT,
                                      database=config.DATABASE)

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute(SQLquerry)
        connection.commit()
        print('done')

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)

    return cursor, connection


def close_connection():
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")


cursor2, connection2 = connect_to_db()
close_connection()


async def add_user(self,
                   id,
                   name,
                   full_name,
                   chat_id,
                   user_id,
                   current__time=60,
                   time_increase=10,
                   increase_in_days=14,
                   increase_day=datetime.datetime.today().date() + timedelta(days=14),
                   times_missed=0,
                   planked_today=False,
                   vacation=False,
                   politeness='polite'
                   ):
    sql = """INSERT INTO plank_schema.Users (
    id,
    name,
    full_name,
    chat_id,
    user_id,
    current__time,
    time_increase,
    increase_in_days,
    increase_day,
    times_missed,
    planked_today,
    vacation,
    politeness) VALUES(
    $1,
    $2,
    $3,
    $4,
    $5,
    $6,
    $7,
    $8,
    $9,
    $10,
    $11,
    $12,
    $13) 
    returning *"""
    return await self.execute(sql, id, name, full_name, chat_id, user_id, current__time, time_increase,
                              increase_in_days, increase_day, times_missed, planked_today, vacation, politeness,
                              fetchrow=True)

async def add_users():
    users = [
        (147258369, 'Oleg', 'DylevichOleg', 123, 456),
        (987654321, 'Kram', 'Kram Kramovich', 123, 741),
        (123456789, 'Andrey', 'Andrey Andreich', 123, 963)
    ]
    list_of_db_users = []
    for id, name, full_name, chat_id, user_id in users:
        user = await db.add_user(id=id, name=name, full_name=full_name, chat_id=chat_id, user_id=user_id)
        list_of_db_users.append(user)

loop.run_until_complete(add_users())