from buffs.LuckyGuyBuff import LuckyGuyBuff
from buffs.ToughGuyBuff import ToughGuyBuff


async def get_all_buffs():
    all_buffs = {
        'tough_guy': 'Рисковый парень',
        'lucky_guy': 'Счастливчик',
    }
    return all_buffs


async def initialize_buff(buff_code):
    names = await get_all_buffs()
    all_buffs = {
        'tough_guy': ToughGuyBuff(code=buff_code, name=names[buff_code]),
        'lucky_guy': LuckyGuyBuff(code=buff_code, name=names[buff_code]),
    }
    return all_buffs[buff_code]