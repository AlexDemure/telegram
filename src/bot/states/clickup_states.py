from aiogram.dispatcher.filters.state import State, StatesGroup


class ConnectionClickUpState(StatesGroup):
    add_click_up_data = State()


