from aiogram.dispatcher.filters.state import State, StatesGroup


class BurndownChartState(StatesGroup):
    choose_space = State()
    choose_folder = State()
    choose_list = State()
