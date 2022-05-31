from buffs.Buff import Buff


class ToughGuyBuff(Buff):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.duration = 14
        self.increase_coefficient = 0.05

    async def describe(self):
        description = 'Включив этот бафф, твое минимальное время будет увеличиваться каждый день на ' + str(
            self.increase_coefficient * 100) + '% в течении ' + str(self.duration) + ' дней. \n' \
            'Ты не сможешь вручную изменить свое минимальное время в этот период. \n' \
            'Если ты выдержишь испытание, то у тебя появится право на 1 день отдыха.'
        return description

