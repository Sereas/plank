from aiogram.dispatcher.filters.state import StatesGroup, State


class MenuStates(StatesGroup):
    set_min_time = State()
    set_time_increase = State()
    set_days_increase = State()
    get_calendar_date = State()
    set_new_name = State()
    previous_date_stat = State()
    free_skip = State()
    test = State()


