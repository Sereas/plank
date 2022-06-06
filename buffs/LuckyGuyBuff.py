from buffs.Buff import Buff
import random

from loader import storage, db


class LuckyGuyBuff(Buff):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.duration = 10
        self.money_delta = 25
        self.base_time = 0
        self.lower_bound = 10
        self.upper_bound = 80

    async def describe(self):
        description = 'Включив этот бафф, каждый день в течении ' + str(self.duration) + ' дней тебе будет предожено' \
                      ' увеличить свое базовое время на рандомное значение (от ' + str(self.lower_bound) + '% до ' + str(self.upper_bound) + '%). \n' \
                      'За каждое согласие, цена твоего следующего пропуска уменьшится' \
                      ' на ' + str(self.money_delta) + ' рублей. За каждый отказ - увеличится на ' + str(self.money_delta) + ' рублей. \n' \
                      'Бездействие будет считаться отказом.'
        return description

    async def today_time(self):
        user = await db.check_if_user_exists(id=self.id)
        rolled_time = await storage.get_data(chat=user['chat_id'], user=(str(user['user_id']) + '_today_time'))
        print(rolled_time)
        if isinstance(rolled_time, int):
            print('Already rolled today, got ' + str(rolled_time))
            today_time = rolled_time
        else:
            possible_time_change = []
            for delta in range(self.lower_bound, self.upper_bound, 5):  # in percents
                possible_time_change.append(delta)

            today_time = random.choice(possible_time_change)
            await storage.set_data(chat=user['chat_id'], user=(str(user['user_id']) + '_today_time'), data=today_time)
        return today_time
