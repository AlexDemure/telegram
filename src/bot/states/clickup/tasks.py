from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateTaskState(StatesGroup):
    add_folder = State()
    add_list = State()
    add_name = State()
    add_desc = State()
    add_assigned = State()
    add_tags = State()
    add_priority = State()
    check_data = State()
    create_task = State()
    add_attachments = State()


class GetTaskState(StatesGroup):
    input_task_id = State()


class GetTaskListByUser(StatesGroup):
    choose_assigned = State()
