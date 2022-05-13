from loader import db


async def get_names(**kwargs):
    user_names = []
    users = await db.select_all_rows_conditions(**kwargs)
    for user in users:
        user_names.append(user['name'])

    return user_names