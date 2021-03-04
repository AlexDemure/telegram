from aiogram.dispatcher.filters.state import State, StatesGroup


class ConnectionClickUpState(StatesGroup):
    get_auth_token = State()
    add_auth_token = State()


