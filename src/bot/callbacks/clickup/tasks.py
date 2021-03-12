from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from src.bot.commands.clickup.tasks import (
    create_task_add_name, create_task_add_tags,
    create_task_add_priority, create_task_check_data,
    create_task_add_list, create_task_send_request, create_task_add_folder,
    get_tasks_by_click_up_user,
    get_task_list_by_project_choose_list as command_get_task_list_by_project_choose_list,
    get_task_list_by_project_choose_task_status as command_get_task_list_by_project_choose_task_status,
    get_task_list_by_project,
    get_task_list_by_project_choose_folder as command_get_task_list_by_project_choose_folder
)
from src.bot.dispatcher import dp
from src.bot.states.clickup.tasks import CreateTaskState, GetTaskListByUser, GetTasksByList


@dp.callback_query_handler(text_contains="spaces", state=CreateTaskState.add_space)
async def choose_space(query: CallbackQuery, state: FSMContext):
    """
    Callback функция - принимает уведомления при выборе Space в Workspace.
    Ожидаемое состояние - Создание задачи, Добавление Space

    Space - список глобальных папок в окружении.
    query = CallbackData("spaces", "id", "name")
    """
    space = query.data.split(':')
    await state.update_data(space_id=space[1], space_name=space[2])

    await create_task_add_folder(query.message, state)  # Переход на этап добавления Folder из выбранного Space


@dp.callback_query_handler(text_contains="folders", state=CreateTaskState.add_folder)
async def choose_folder(query: CallbackQuery, state: FSMContext):
    """
    Callback функция - принимает уведомления при выборе Folder в Workspace.
    Ожидаемое состояние - Создание задачи, Добавление Folder

    Folder - список папок в Space окружении.
    query = CallbackData("folders", "id", "name")
    """
    folder = query.data.split(':')
    await state.update_data(folder_id=folder[1], folder_name=folder[2])

    await create_task_add_list(query.message, state)  # Переход на этап добавления List из выбранного Folder


@dp.callback_query_handler(text_contains="lists", state=CreateTaskState.add_list)
async def choose_list(query: CallbackQuery, state: FSMContext):
    """
    Callback функция - принимает уведомления при выборе List в Folder.
    Ожидаемое состояние - Создание задачи, Добавление List

    List - один из элементов Folder, List могут быть спринты, backlogs, bugs.
    query = CallbackData("lists", "id", "name")
    """
    list = query.data.split(':')
    await state.update_data(list_id=list[1], list_name=list[2])

    await create_task_add_name(query.message, state)  # Переход на этап заполнения данных по задаче.


@dp.callback_query_handler(text_contains="assigned", state=CreateTaskState.add_assigned)
async def choose_assigned(query: CallbackQuery, state: FSMContext):
    """
    Callback функция - принимает уведомления при выборе Исполнителя по задаче.
    Ожидаемое состояние - Создание задачи, Добавление исполнителя

    Логика написана под одного исполнителя на задачу хотя ClickUp поддерживает множественное количество исполнителей.
    query = CallbackData("assigned", "id", "username")
    """
    assigned = query.data.split(':')
    await state.update_data(click_up_user_id=assigned[1], click_up_username=assigned[2])

    await create_task_add_tags(query.message, state)  # Переход на этап выбора тегов по задаче.


@dp.callback_query_handler(text_contains="tags", state=[CreateTaskState.add_tags, CreateTaskState.add_priority])
async def choose_tags(query: CallbackQuery, state: FSMContext):
    """
    Callback функция - принимает уведомления при выборе Тегов к задаче.
    Ожидаемое состояние - Создание задачи, Добавление тегов или Добавление приоритета.
    состояние "Добавление приоритета" - ожидается для возможности установки нескольких тегов из списка к задаче.

    query = CallbackData("tags", "name")
    """
    tag = query.data.split(':')[1]
    async with state.proxy() as data:

        if data.get('tags', None) is None:  # Если в callback зашли впервый раз то создаем объект.
            data['tags'] = []

        data['tags'].append(tag)
        data['tags'] = list(set(data['tags']))  # Необходимо для уникальности тегов в списке

        print(data['tags'])

    await create_task_add_priority(query.message, state)  # Переход на этап установки приоритета


@dp.callback_query_handler(text_contains="priorities", state=CreateTaskState.add_priority)
async def choose_priority(query: CallbackQuery, state: FSMContext):
    """
    Callback функция - принимает уведомления при выборе Приоритета к задаче.
    Ожидаемое состояние - Создание задачи, Добавление приоритета.

    query = CallbackData("priorities", "name")
    """
    priority = query.data.split(':')[1]
    await state.update_data(priority=priority)

    await create_task_check_data(query.message, state)  # Переход на этап проверки данных


@dp.callback_query_handler(text_contains="create_task", state=CreateTaskState.check_data)
async def check_task_data(query: CallbackQuery, state: FSMContext):
    """
    Callback функция - принимает уведомления при выборе решения по задаче.
    Решением по задаче может быть "Создать" или "Отменить".
    Ожидаемое состояние - Создание задачи, Проверка данных.

    query = CallbackData("create_task", "action")
    """
    action = query.data.split(':')[1]
    await state.update_data(action=action)

    await create_task_send_request(query.message, state)  # Переход на этап отправки запроса на создание задачи.


@dp.callback_query_handler(text_contains="assigned", state=GetTaskListByUser.choose_assigned)
async def get_task_by_user_choose_assigned(query: CallbackQuery, state: FSMContext):
    """
    Callback функция - принимает уведомления при выборе исполнителя по задачам.
    Ожидаемое состояние - Получение списка задач по клиенту ClickUp, Выбор исполнителя.

    query = CallbackData("assigned", "id", "username")
    """
    assigned = query.data.split(':')
    await state.update_data(click_up_user_id=assigned[1], click_up_username=assigned[2])

    await get_tasks_by_click_up_user(query.message, state)  # Переход на этап получения списка задач.


@dp.callback_query_handler(text_contains="spaces", state=GetTasksByList.choose_space)
async def get_task_list_by_project_choose_space(query: CallbackQuery, state: FSMContext):
    """
    Callback функция - принимает уведомления при выборе Space в Workspace.
    Ожидаемое состояние - Получение списка задач по проекту, Выбор Space

    Space - список глобальных папок в окружении.
    query = CallbackData("spaces", "id", "name")
    """
    space = query.data.split(':')
    await state.update_data(space_id=space[1], space_name=space[2])

    await command_get_task_list_by_project_choose_folder(query.message, state)  # Переход на этап выбор Folder из выбранного Space


@dp.callback_query_handler(text_contains="folders", state=GetTasksByList.choose_folder)
async def get_task_list_by_project_choose_folder(query: CallbackQuery, state: FSMContext):
    """
    Callback функция - принимает уведомления при выборе Folder в Workspace.
    Ожидаемое состояние - Получение списка задач по проекту, Выбор Folder

    Folder - список папок в Space окружении.
    query = CallbackData("folders", "id", "name")
    """
    folder = query.data.split(':')
    await state.update_data(folder_id=folder[1], folder_name=folder[2])

    await command_get_task_list_by_project_choose_list(query.message, state)  # Переход на этап выбора List из выбранного Folder


@dp.callback_query_handler(text_contains="lists", state=GetTasksByList.choose_list)
async def get_task_list_by_project_choose_list(query: CallbackQuery, state: FSMContext):
    """
    Callback функция - принимает уведомления при выборе List в Folder.
    Ожидаемое состояние - Получение списка задач по проекту, Выбор List

    List - один из элементов Folder, List могут быть спринты, backlogs, bugs.
    query = CallbackData("lists", "id", "name")
    """
    list = query.data.split(':')
    await state.update_data(list_id=list[1], list_name=list[2])

    await command_get_task_list_by_project_choose_task_status(query.message, state)  # Переход на этап выбора статуса задачи.


@dp.callback_query_handler(text_contains="task_status", state=GetTasksByList.choose_task_status)
async def get_task_list_by_project_choose_task_status(query: CallbackQuery, state: FSMContext):
    """
    Callback функция - принимает уведомления при выборе Типа задач которые необходимо отобразить.
    Ожидаемое состояние - Получение списка задач по проекту, Выбор типа задач.

    query = CallbackData("task_status", "task_group")
    """
    task_group = query.data.split(':')
    await state.update_data(task_group=task_group[-1])

    await get_task_list_by_project(query.message, state)  # Переход на сбор задач.
