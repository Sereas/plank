import datetime


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

