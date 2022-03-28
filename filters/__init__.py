from aiogram import Dispatcher
from .admins import AdminFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)

