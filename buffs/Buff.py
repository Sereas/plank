import datetime

from loader import db_buffs


class Buff:
    def __init__(self, **kwargs):

        try:
            self.id = kwargs['id']
        except KeyError:
            self.id = None

        try:
            self.buff_id = kwargs['buff_id']
        except KeyError:
            self.buff_id = None

        try:
            self.name = kwargs['name']
        except KeyError:
            self.name = None

        try:
            self.code = kwargs['code']
        except KeyError:
            self.code = None

        try:
            self.date_buff_started = kwargs['date_buff_started']
        except KeyError:
            self.date_buff_started = datetime.datetime.today().date()

        try:
            self.date_buff_ended = kwargs['date_buff_ended']
        except KeyError:
            self.date_buff_ended = None

        try:
            self.reason_buff_ended = kwargs['reason_buff_ended']
        except KeyError:
            self.reason_buff_ended = None

        try:
            self.is_active = kwargs['is_active']
        except KeyError:
            self.is_active = False

        try:
            self.duration = kwargs['duration']
        except KeyError:
            self.duration = None

    async def load_existing_buff(self, id):
        self.id = id
        existing_buff = await db_buffs.select_row(table_name='Buffs',
                                                  id=self.id,
                                                  is_active=True)
        if existing_buff is not None:
            self.buff_id = existing_buff['buff_id']
            self.name = existing_buff['name']
            self.code = existing_buff['code']
            self.date_buff_started = existing_buff['date_buff_started']
            self.date_buff_ended = existing_buff['date_buff_ended']
            self.reason_buff_ended = existing_buff['reason_buff_ended']
            self.is_active = existing_buff['is_active']
        else:
            print('This user does not have active buffs')

    async def describe(self):
        pass

    async def buff_action(self, **kwargs):
        pass

    async def on_start(self, **kwargs):
        print('No immediate action')
        pass

    async def activate(self, id):
        await db_buffs.add_buff(id=id,
                                name=self.name,
                                code=self.code,
                                date_buff_started=self.date_buff_started,
                                is_active=True)

    async def cancel(self, date_buff_ended, reason_buff_ended):
        await db_buffs.update_buff(parameter='is_active',
                                   new_value=False,
                                   id=self.id,
                                   buff_id=self.buff_id)
        await db_buffs.update_buff(parameter='date_buff_ended',
                                   new_value=date_buff_ended,
                                   id=self.id,
                                   buff_id=self.buff_id)
        await db_buffs.update_buff(parameter='reason_buff_ended',
                                   new_value=reason_buff_ended,
                                   id=self.id,
                                   buff_id=self.buff_id)

    async def is_expired(self):
        expiration_date = (self.date_buff_started + datetime.timedelta(days=self.duration)).date()
        today = datetime.datetime.today().date()
        days_left = (expiration_date - today).days
        if today > expiration_date:
            expired = True
            await db_buffs.update_buff(parameter='is_active',
                                       new_value=False,
                                       id=self.id,
                                       buff_id=self.buff_id)
            await db_buffs.update_buff(parameter='date_buff_ended',
                                       new_value=today,
                                       id=self.id,
                                       buff_id=self.buff_id)
            await db_buffs.update_buff(parameter='reason_buff_ended',
                                       new_value='expired',
                                       id=self.id,
                                       buff_id=self.buff_id)
        else:
            expired = False
        return expired, days_left
