from buffs.Buff import Buff


class TestBuff(Buff):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.duration = 14
        self.increase_coefficient = 0.05

    async def describe(self):
        description = 'Test message hey hey'
        return description