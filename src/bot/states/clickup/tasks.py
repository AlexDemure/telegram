from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateTaskState(StatesGroup):
    add_space = State()
    add_folder = State()
    add_list = State()
    add_name = State()
    add_desc = State()
    add_assigned = State()
    add_tags = State()
    add_priority = State()
    check_data = State()
    create_task = State()


class GetTaskState(StatesGroup):
    input_task_id = State()
    task_control = State()
    add_comment = State()


class GetTaskListByUser(StatesGroup):
    choose_assigned = State()


class GetTasksByList(StatesGroup):
    choose_space = State()
    choose_folder = State()
    choose_list = State()
    choose_task_status = State()
