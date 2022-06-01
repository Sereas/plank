from buffs.Buff import Buff
from loader import db, bot


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

    async def buff_action(self):
        expired, days_left = await self.is_expired()
        user = await db.check_if_user_exists(id=self.id)
        if not expired:
            current_time = user['current__time']
            new_time = int((1 + self.increase_coefficient) * current_time)
            await db.update_parameter(parameter='current__time',
                                      new_value=new_time,
                                      user_id=user['user_id'],
                                      chat_id=user['chat_id'])
            await bot.send_message(chat_id=user['chat_id'],
                                   text='Поздравляю, ' + user['name'] + '! В результате действия '
                                         'баффа "' + self.name + '" твое время увеличилось и теперь составляет ' + str(new_time) + ' секунд. \n'
                                         'Продолжай в том же духе, осталось всего ' + str(days_left) + ' дней!')
        else:
            await bot.send_message(chat_id=user['chat_id'],
                                   text='Поздравляю, ' + user['name'] + '! Ты уверенно справился с испытанием '
                                        + self.name + ' и заслужил право на 1 день отдыха!')
            current_free_skips = user['free_skips']
            current_free_skips += 1
            await db.update_parameter(parameter='free_skips',
                                      new_value=current_free_skips,
                                      user_id=user['user_id'],
                                      chat_id=user['chat_id'])
