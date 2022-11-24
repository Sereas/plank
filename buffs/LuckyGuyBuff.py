import datetime

from buffs.Buff import Buff
import random

from loader import storage, db, bot, db_logs


class LuckyGuyBuff(Buff):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.duration = 10
        self.money_delta = 25
        self.lower_bound = 10
        self.upper_bound = 80

    async def describe(self):
        description = 'Включив этот бафф, каждый день в течении ' + str(self.duration) + ' дней тебе будет предожено' \
                      ' увеличить свое базовое время на рандомное значение (от ' + str(self.lower_bound) + '% до ' + str(self.upper_bound) + '%). \n' \
                      'За каждое согласие, цена твоего следующего пропуска уменьшится' \
                      ' на ' + str(self.money_delta) + ' рублей. За каждый отказ - увеличится на ' + str(self.money_delta) + ' рублей. \n' \
                      'Бездействие будет считаться отказом.'
        return description

    async def on_start(self):
        user = await db.check_if_user_exists(id=self.id)
        mention = "[" + user['name'] + "](tg://user?id=" + str(user['user_id']) + ")"
        today_time = await self.today_time()
        if today_time <= 40:
            roll_god_attitude = 'благосклоны'
        else:
            roll_god_attitude = 'не благосклоны'
        await bot.send_message(chat_id=user['chat_id'],
                               text='Боги ролла к тебе сегодня ' + roll_god_attitude + ', ' + mention + '! \n'
                                     'Они предлагают тебе увеличить время на ' + str(
                                     today_time) + '%\n'
                                     'Ты можешь согласиться или отказаться в "Использовать бафф" ==> "Счастливчик" ==> "Изменение времени на сегодня" \n'
                                     'Напоминаю, что бездействие равно отказу.',
                               parse_mode="Markdown")

    async def buff_action(self, **kwargs):
        expired, days_left = await self.is_expired()
        user = await db.check_if_user_exists(id=self.id)
        mention = "[" + user['name'] + "](tg://user?id=" + str(user['user_id']) + ")"
        today = datetime.datetime.today()
        if not expired:
            if user['vacation']:
                await self.sick_while_buff()
                await bot.send_message(chat_id=user['chat_id'],
                                       text='Дорогой, ' + user['name'] + '! Ты на больничном, а значит время действия бафа не уменьшается!')
            else:
                accepted = await self.get_state_accepted()
                if accepted:
                    base_time = await self.get_state_base_time()
                    await db.update_parameter(parameter='current__time',
                                              new_value=base_time,
                                              user_id=user['user_id'],
                                              chat_id=user['chat_id'])

                    new_payment = user['next_payment_amount'] - self.money_delta
                    await db.update_parameter(parameter='next_payment_amount',
                                              new_value=new_payment,
                                              user_id=user['user_id'],
                                              chat_id=user['chat_id'])

                    await bot.send_message(chat_id=user['chat_id'],
                                           text='Поздравляю, ' + mention + ', с еще одним успешным днем в баффе!'
                                                 ' Вернул твое базовое время в ' + str(base_time) + ' секунд и уменьшил'
                                                 ' твой следующий платеж до ' + str(new_payment) + ' рублей. \n'
                                                 'Так держать, осталось всего ' + str(days_left) + ' дней!',
                                           parse_mode="Markdown")

                else:
                    new_payment = user['next_payment_amount'] + self.money_delta
                    await db.update_parameter(parameter='next_payment_amount',
                                              new_value=new_payment,
                                              user_id=user['user_id'],
                                              chat_id=user['chat_id'])

                    await bot.send_message(chat_id=user['chat_id'],
                                           text='К сожалению, ' + mention + ', ты не осмелился увеличить время как'
                                                ' того велел бафф и теперь твой следующий платеж составит '
                                                + str(new_payment) + ' рублей. \n'
                                                'Но ничего, бафф еще будет действовать ' + str(days_left) + ' дней, ты наверстаешь упущенное =)',
                                           parse_mode="Markdown")

                await self.reset_all_states()
                today_time = await self.today_time()
                if today_time <= 40:
                    roll_god_attitude = 'благосклоны'
                else:
                    roll_god_attitude = 'не благосклоны'
                await bot.send_message(chat_id=user['chat_id'],
                                       text='Боги ролла к тебе сегодня ' + str(today.strftime("%d %b %Y")) + ' ' + roll_god_attitude + ', ' + mention + '! \n'
                                            'Они предлагают тебе увеличить время на ' + str(today_time) + '%\n'
                                            'Ты можешь согласиться или отказаться в "Использовать бафф" ==> "Счастливчик" ==> "Изменение времени на сегодня" \n'
                                            'Напоминаю, что бездействие равно отказу.',
                                       parse_mode="Markdown")

        elif expired:
            await bot.send_message(chat_id=user['chat_id'],
                                   text='Ура, ' + mention + '! Действие баффа "Счастливчик" закончилось!',
                                   parse_mode="Markdown")
            await self.reset_all_states()

    async def set_state_today_time(self, today_time):
        user = await db.check_if_user_exists(id=self.id)
        await storage.set_data(chat=user['chat_id'], user=(str(user['user_id']) + '_today_time'), data=today_time)

    async def get_state_today_time(self):
        user = await db.check_if_user_exists(id=self.id)
        rolled_time = await storage.get_data(chat=user['chat_id'], user=(str(user['user_id']) + '_today_time'))
        return rolled_time

    async def today_time(self):
        rolled_time = await self.get_state_today_time()
        print(rolled_time)
        if isinstance(rolled_time, int):  # already rolled and saved time
            print('Already rolled today, got ' + str(rolled_time))
            today_time = rolled_time
        else:
            possible_time_change = []
            for delta in range(self.lower_bound, self.upper_bound, 5):  # in percents
                possible_time_change.append(delta)

            today_time = random.choice(possible_time_change)
            await self.set_state_today_time(today_time=today_time)
        return today_time

    async def set_state_base_time(self):
        user = await db.check_if_user_exists(id=self.id)
        await storage.set_data(chat=user['chat_id'], user=(str(user['user_id']) + '_base_time'), data=user['current__time'])

    async def get_state_base_time(self):
        user = await db.check_if_user_exists(id=self.id)
        base_time = await storage.get_data(chat=user['chat_id'], user=(str(user['user_id']) + '_base_time'))
        return base_time

    async def set_state_accepted(self, data=True):
        user = await db.check_if_user_exists(id=self.id)
        await storage.set_data(chat=user['chat_id'], user=(str(user['user_id']) + '_accepted'), data=data)

    async def get_state_accepted(self):
        user = await db.check_if_user_exists(id=self.id)
        accepted = await storage.get_data(chat=user['chat_id'], user=(str(user['user_id']) + '_accepted'))
        return accepted

    async def reset_all_states(self):
        user = await db.check_if_user_exists(id=self.id)
        await storage.reset_data(chat=user['chat_id'], user=(str(user['user_id']) + '_base_time'))
        await storage.reset_data(chat=user['chat_id'], user=(str(user['user_id']) + '_today_time'))
        await storage.reset_data(chat=user['chat_id'], user=(str(user['user_id']) + '_accepted'))
