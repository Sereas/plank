from aiogram import Dispatcher
from .admins import AdminFilter
from .buff_filters import ToughGuyFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(ToughGuyFilter)


