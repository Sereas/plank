import datetime

from aiogram.types import CallbackQuery

from handlers.groups.day_stats import get_day_stats
from handlers.groups.get_calendar_event import get_calendar


async def show_past_date_info(callback: CallbackQuery):
    await get_calendar(callback=callback)

