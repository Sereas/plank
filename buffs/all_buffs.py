from buffs.TestBuff import TestBuff
from buffs.ToughGuyBuff import ToughGuyBuff


async def get_all_buffs():
    all_buffs = {
        'tough_guy': 'Рисковый парень',
        'test_buff': 'Test'
    }
    return all_buffs


async def initialize_buff(buff_code):
    names = await get_all_buffs()
    all_buffs = {
        'tough_guy': ToughGuyBuff(code=buff_code, name=names[buff_code]),
        'test_buff': TestBuff(code=buff_code, name=names[buff_code])
    }
    return all_buffs[buff_code]