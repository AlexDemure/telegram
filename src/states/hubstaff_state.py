from aiogram.dispatcher.filters.state import State, StatesGroup


class ConnectionHubStaffState(StatesGroup):
    get_auth_token = State()
    add_auth_token = State()


