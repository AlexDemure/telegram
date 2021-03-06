import tempfile
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode, ReplyKeyboardRemove

from src.apps.clickup.logic import (
    get_user_tasks, get_user_tasks_with_unset_time, create_task,
    get_members, get_user_folders_by_space_id, get_lists_by_folder, get_task_by_id,
    get_tasks, get_user_spaces, get_task_comments, add_task_comment, add_task_attachment
)
from src.apps.users.logic import get_user
from src.bot.dispatcher import bot, dp
from src.bot.keyboards import start as start_keyboards
from src.bot.keyboards.clickup import menu as menu_click_up_keyboards
from src.bot.keyboards.clickup import tasks as tasks_click_up_keyboards
from src.bot.messages.clickup.tasks import (
    prepare_response_list_tasks, prepare_response_create_task_check_data,
    prepare_response_list_tasks_with_unset_time, prepare_response_task_data,
    prepare_response_task_comments
)
from src.bot.states.clickup.tasks import CreateTaskState, GetTaskState, GetTaskListByUser, GetTasksByList
from src.submodules.clickup.enums import Tags, Priority, Teams, ClickUpTaskStatusType
from src.submodules.clickup.schemas import ClickUpCreateTask, SpaceData


@dp.message_handler(Text(equals=[menu_click_up_keyboards.MenuClickUpKeysEnum.main.value]), state="*")
async def start_task_menu(message: types.Message, state: FSMContext):
    """
    Главное меню с ClickUp
    :return: Клавиатуру с выбором "Основных действий" (Управление задачами, Мои задачи)
    """
    await state.reset_state()

    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    await message.answer(
        f"Меню по ClickUp:",
        parse_mode=ParseMode.HTML,
        reply_markup=menu_click_up_keyboards.keyboards
    )


@dp.message_handler(Text(equals=[menu_click_up_keyboards.MenuClickUpKeysEnum.me_task_menu.value]), state=None)
async def me_task_menu(message: types.Message):
    """
    Персональное меню с задачами ClickUp
    :return: Клавиатуру "Мои задачи" (Список задач и т.д)
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    await message.answer(
        f"Меню по моим задачам ClickUp:",
        parse_mode=ParseMode.HTML,
        reply_markup=tasks_click_up_keyboards.me_menu_keyboards
    )


@dp.message_handler(Text(equals=[menu_click_up_keyboards.MenuClickUpKeysEnum.task_manager.value]), state=None)
async def manager_task_menu(message: types.Message):
    """
    Менеджер меню ClickUp
    :return: Клавиатуру "Управление задачами" в которую входит (Создать, Найти задачу и т.д.)
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    await message.answer(
        f"Меню по ClickUp:",
        parse_mode=ParseMode.HTML,
        reply_markup=tasks_click_up_keyboards.task_manager_keyboards
    )


@dp.message_handler(Text(equals=[tasks_click_up_keyboards.MeMenuClickUpKeysEnum.task_list.value]), state=None)
async def get_my_tasks(message: types.Message):
    """
    Handler по нажатию Кнопки "Мои задачи".
    Поиск происходит по текущему пользователю.

    :return: Список задач по пользователю.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    user_tasks = await get_user_tasks(user)
    response = prepare_response_list_tasks(user_tasks)

    await message.answer(
        f"{response}",
        parse_mode=ParseMode.HTML,
        reply_markup=tasks_click_up_keyboards.me_menu_keyboards
    )


@dp.message_handler(Text(equals=[tasks_click_up_keyboards.MeMenuClickUpKeysEnum.task_list_with_unset_time.value]),
                    state=None)
async def get_my_tasks_with_unset_time(message: types.Message):
    """
    Handler по нажатию Кнопки "Мои задачи без запланированного времени".
    Поиск происходит по текущему пользователю.

    :return: Список задач по пользователю в которых не проставлено time_estimate в ClickUp.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден. Пожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    user_tasks = await get_user_tasks_with_unset_time(user)
    response = prepare_response_list_tasks_with_unset_time(user_tasks)

    await message.answer(
        f"{response}",
        parse_mode=ParseMode.HTML,
        reply_markup=tasks_click_up_keyboards.me_menu_keyboards
    )


@dp.message_handler(Text(equals=[tasks_click_up_keyboards.TaskManagerClickUpKeysEnum.get_task.value]), state=None)
async def get_task_input_id(message: types.Message):
    """
    Шаг №1 Ввод ID задачи.
    Handler по нажатию Кнопки "Поиск задачи".
    Поиск происходит по ID задачи.

    :return: Ничего не возвращает. Ожидается ввод пользователя.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    await message.reply(
        f"Введите ID задачи или ссылку на нее:",
        reply_markup=ReplyKeyboardRemove()
    )

    await GetTaskState.input_task_id.set()


@dp.message_handler(state=GetTaskState.input_task_id)
async def get_task_find_task(message: types.Message, state: FSMContext):
    """
    Шаг №2 Прием данных от клиента и попытка поиска задачи.
    Handler по нажатию Кнопки "Поиск задачи".
    Поиск происходит по ID задачи.

    :return: Опциональный возврат данных. Информация по задаче или "Задача не найдена".
    :return: Список InlineButtons.
    Ожидается выбор пользователя и уведомление на callback handler.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        await state.finish()
        return

    link_items = message.text.split("https://app.clickup.com/t/")
    if len(link_items) > 0:
        task_id = link_items[-1]
    else:
        task_id = message.text

    task, members = await get_task_by_id(user, task_id)
    if task is None:
        await message.reply(
            f"Задача с таким ID не найдена.",
            reply_markup=tasks_click_up_keyboards.task_manager_keyboards
        )
        await state.finish()
        return

    response = prepare_response_task_data(task, members)

    choice = tasks_click_up_keyboards.generate_inline_buttons_for_click_up_task_control()
    await bot.send_message(
        message.chat.id,
        f"{response}\nВыберите дальнейшее действие с задачей:",
        parse_mode=ParseMode.HTML,
        reply_markup=choice
    )

    await state.update_data(task_id=task.id)

    await GetTaskState.task_control.set()


async def get_task_choose_action(message: types.Message, state: FSMContext):
    """
    Шаг №2 Выбор проекта куда хотим добавить задачу.
    Функция которая вызывается из Callback Handler, get_task_choose_action

    :return: Опциональный возврат данных. Список комментарьев, Добавленный комментарий.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    data = await state.get_data()

    if data['action'] == "add_comment":
        await bot.send_message(
            message.chat.id,
            "Текст комментария:",
            reply_markup=ReplyKeyboardRemove()
        )
        await GetTaskState.add_comment.set()
        return

    elif data['action'] == "add_file":
        await bot.send_message(
            message.chat.id,
            "Вставьте документ:",
            reply_markup=ReplyKeyboardRemove()
        )
        await GetTaskState.add_file.set()
        return

    elif data['action'] == "cancel":
        response = "Отмена"

    elif data['action'] == "list_comment":
        comments = await get_task_comments(user, data['task_id'])
        response = prepare_response_task_comments(comments)

    else:
        raise ValueError

    await bot.send_message(
        message.chat.id,
        response,
        parse_mode=ParseMode.HTML,
        reply_markup=tasks_click_up_keyboards.task_manager_keyboards
    )

    await state.finish()


@dp.message_handler(state=GetTaskState.add_comment)
async def get_task_add_comment(message: types.Message, state: FSMContext):
    """
    Шаг №3 Ввод комментария к задаче. Добавление комментария к задаче.
    Прием ввода от пользователя.

    :return: Текст с упешным добавление комментария.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    data = await state.get_data()

    await add_task_comment(user, data['task_id'], message.text)

    await bot.send_message(
        message.chat.id,
        "Комментарий успешно добавлен.",
        reply_markup=tasks_click_up_keyboards.task_manager_keyboards
    )

    await state.finish()


@dp.message_handler(
    state=GetTaskState.add_file,
    content_types=['photo', 'document']
)
async def get_task_add_file(message: types.Message, state: FSMContext):
    """
    Добавление файла к задаче. Прием ввода от пользователя.

    :return: Текст с упешным добавление файла.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    data = await state.get_data()

    if message.photo is not None and len(message.photo) > 0:
        with tempfile.NamedTemporaryFile(suffix=f'.jpeg') as temp_file:
            await message.photo[-1].download(temp_file.name)
            with open(temp_file.name, "rb") as file:
                await add_task_attachment(user, data['task_id'], file)

    elif message.document is not None:
        with tempfile.NamedTemporaryFile(suffix=f'.{message.document.file_name.split(".")[-1]}') as temp_file:
            await message.document.download(temp_file.name)
            with open(temp_file.name, "rb") as file:
                await add_task_attachment(user, data['task_id'], file)

    choice = tasks_click_up_keyboards.generate_inline_buttons_for_click_up_add_files()

    await bot.send_message(
        message.chat.id,
        "Документ успешно добавлен.",
        reply_markup=choice
    )

    await GetTaskState.task_control.set()


@dp.message_handler(Text(equals=[tasks_click_up_keyboards.TaskManagerClickUpKeysEnum.create_task.value]), state=None)
async def create_task_add_space(message: types.Message):
    """
    Шаг №1 Выбор проекта куда хотим добавить задачу.
    Handler по нажатию Кнопки "Создать задачу".

    :return: Список InlineButtons.
    Ожидается выбор пользователя и уведомление на callback handler.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    data = await get_user_spaces(user)
    choices = tasks_click_up_keyboards.generate_inline_buttons_for_click_up_spaces(data)
    for choice in choices:
        await bot.send_message(
            message.chat.id,
            f"{choice['team_name']}",
            reply_markup=choice['keyboards']
        )

    await CreateTaskState.add_space.set()


async def create_task_add_folder(message: types.Message, state: FSMContext):
    """
    Шаг №2 Выбор проекта куда хотим добавить задачу.
    Функция которая вызывается из Callback Handler, choose_space

    :return: Список InlineButtons.
    Ожидается выбор пользователя и уведомление на callback handler.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    data = await state.get_data()

    folders = await get_user_folders_by_space_id(user, data['space_id'])

    choice = tasks_click_up_keyboards.generate_inline_buttons_for_click_up_folders(
        SpaceData(
            id=data['space_id'],
            name=data['space_name'],
            folders=folders
        )
    )

    await bot.send_message(
        message.chat.id,
        f"{data['space_name']}",
        reply_markup=choice
    )

    await CreateTaskState.add_folder.set()


async def create_task_add_list(message: types.Message, state: FSMContext):
    """
    Шаг №3 Выбор списка (bugs, backlogs, sprint) из Проекта куда хотим добавить задачу.
    Функция которая вызывается из Callback Handler, choose_folder

    :return: Список InlineButtons.
    Ожидается выбор пользователя и уведомление на callback handler.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    data = await state.get_data()

    folder = await get_lists_by_folder(user, data['folder_id'])
    choice = tasks_click_up_keyboards.generate_inline_buttons_for_click_up_lists(folder)

    await bot.send_message(message.chat.id, f"{folder.name}", reply_markup=choice['keyboards'])

    await CreateTaskState.add_list.set()


async def create_task_add_name(message: types.Message, state: FSMContext):
    """
    Шаг №4 Заполнение данных о задачи. Добавление названия задачи.
    Функция которая вызывается из Callback Handler, choose_list

    :return: Ничего не возвращает. Ожидается ввод пользователя.
    """
    await message.reply(
        f"Создание задачи.\nВведите заголовок задачи:",
        reply_markup=ReplyKeyboardRemove()
    )

    await CreateTaskState.add_desc.set()


@dp.message_handler(state=CreateTaskState.add_desc)
async def create_task_add_desc(message: types.Message, state: FSMContext):
    """
    Шаг №5 Заполнение данных о задачи. Добавление описания задачи.
    Прием ввода от пользователя.

    :return: Ничего не возвращает. Ожидается ввод пользователя.
    """
    await state.update_data(name=message.text)

    await message.reply(
        f"Введите описание задачи:",
        reply_markup=ReplyKeyboardRemove()
    )

    await CreateTaskState.add_assigned.set()


@dp.message_handler(state=CreateTaskState.add_assigned)
async def create_task_add_assigned(message: types.Message, state: FSMContext):
    """
    Шаг №6 Выбор исполнителя по задаче.

    :return: Список InlineButtons.
    Ожидается выбор пользователя и уведомление на callback handler.
    """
    await state.update_data(desc=message.text)

    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        await state.finish()
        return

    member_groups = await get_members(user)
    choices = tasks_click_up_keyboards.generate_inline_buttons_for_click_up_members(member_groups)
    for choice in choices:
        await bot.send_message(
            message.chat.id,
            f"{choice['member_group']}",
            reply_markup=choice['keyboards']
        )


async def create_task_add_tags(message: types.Message, state: FSMContext):
    """
    Шаг №7 Заполнение данных о задачи. Добавление тегов к задаче.
    Функция которая вызывается из Callback Handler, choose_assigned

    :return: Список InlineButtons.
    Ожидается выбор пользователя и уведомление на callback handler.
    """
    choice = tasks_click_up_keyboards.generate_inline_buttons_for_click_up_tags(
        tags=[(e.value, e.preview_name) for e in Tags]
    )
    await bot.send_message(message.chat.id, f"{choice['response']}", reply_markup=choice['keyboards'])
    await CreateTaskState.add_tags.set()


async def create_task_add_priority(message: types.Message, state: FSMContext):
    """
    Шаг №8 Заполнение данных о задачи. Добавление приоритета к задаче.
    Функция которая вызывается из Callback Handler, choose_tags

    :return: Список InlineButtons.
    Ожидается выбор пользователя и уведомление на callback handler.
    """
    state = await state.get_state()

    if state == CreateTaskState.add_priority.state:
        await bot.send_message(message.chat.id, f"Выберите приоритет:", reply_markup=ReplyKeyboardRemove())
        return

    choice = tasks_click_up_keyboards.generate_inline_buttons_for_click_up_priority(
        priorities=[(e.value, e.preview_name) for e in Priority if e != Priority.NOT_SET]
    )

    await bot.send_message(message.chat.id, f"{choice['response']}", reply_markup=choice['keyboards'])
    await CreateTaskState.add_priority.set()


async def create_task_check_data(message: types.Message, state: FSMContext):
    """
    Шаг №9 Проверка данных.
    Функция которая вызывается из Callback Handler, choose_priority

    :return: Список InlineButtons.
    Ожидается выбор пользователя и уведомление на callback handler.
    """
    data = await state.get_data()
    response = prepare_response_create_task_check_data(data)
    choice = tasks_click_up_keyboards.generate_inline_buttons_for_click_up_check_data()

    await bot.send_message(
        message.chat.id, f"{response}",
        parse_mode=ParseMode.HTML,
        reply_markup=choice
    )

    await CreateTaskState.check_data.set()


async def create_task_send_request(message: types.Message, state: FSMContext):
    """
    Шаг №10 Финальное действие по задаче Создать или Отменить создание.
    Функция которая вызывается из Callback Handler, check_task_data
    Создать - происходит запрос на создание таска.
    Отменить - происходит возврат в меню по управлению задачами.

    Примерный state на данном этапе
    {
        'folder_id': '15217167', 'folder_name': 'Podcaster',
        'list_id': '33952819', 'list_name': 'Backlog',
        'name': '123', 'desc': '321',
        'click_up_user_id': '6655746', 'click_up_username': 'Alex Demure',
        'tags': ['supporting'], 'priority': 'high'
    }:
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        await state.finish()
        return

    data = await state.get_data()

    if data['action'] == "Отменить":
        await bot.send_message(
            message.chat.id,
            f"Создание задачи отменено.",
            reply_markup=tasks_click_up_keyboards.task_manager_keyboards
        )
        await state.finish()
        return

    new_task = await create_task(
        user_data=user,
        list_id=data['list_id'],
        task_data=ClickUpCreateTask(
            name=data['name'],
            description=data['desc'],
            assignees=[int(data['click_up_user_id']), ],
            tags=[Tags(x).value for x in data['tags']],
            priority=Priority(data['priority']).clickup_priority_value
        )
    )

    choice = tasks_click_up_keyboards.generate_inline_buttons_for_click_up_task_control(is_new_task=True)
    await bot.send_message(
        message.chat.id,
        f"Задача создана ID: {new_task['url']}.",
        reply_markup=choice
    )

    await state.update_data(task_id=new_task['id'])
    await GetTaskState.task_control.set()


@dp.message_handler(Text(equals=[tasks_click_up_keyboards.TaskManagerClickUpKeysEnum.task_list_by_user.value]),
                    state=None)
async def get_tasks_by_click_up_user_choose_assigned(message: types.Message):
    """
    Шаг №1 Выбор исполнителя.
    Получение списка задач по определенному пользователю.

    :return: Список InlineButtons.
    Ожидается выбор пользователя и уведомление на callback handler.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    if user.click_up.role not in [Teams.admin.value, Teams.owner.value]:
        await message.reply(
            f"У вас недостаточно прав для этой команды.",
            reply_markup=tasks_click_up_keyboards.task_manager_keyboards
        )
        return

    member_groups = await get_members(user)
    choices = tasks_click_up_keyboards.generate_inline_buttons_for_click_up_members(member_groups)
    for choice in choices:
        await bot.send_message(
            message.chat.id,
            f"{choice['member_group']}",
            reply_markup=choice['keyboards']
        )

    await GetTaskListByUser.choose_assigned.set()


async def get_tasks_by_click_up_user(message: types.Message, state: FSMContext):
    """Получение списка задач по id-пользователя из телеграмм."""
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    data = await state.get_data()

    user_tasks = await get_user_tasks(user, data['click_up_user_id'])
    response = prepare_response_list_tasks(user_tasks)

    await message.answer(
        f"{data['click_up_username']} {response}",
        parse_mode=ParseMode.HTML,
        reply_markup=tasks_click_up_keyboards.task_manager_keyboards
    )
    await state.finish()


@dp.message_handler(Text(equals=[tasks_click_up_keyboards.TaskManagerClickUpKeysEnum.task_list_by_project.value]),
                    state=None)
async def get_task_list_by_project_choose_space(message: types.Message):
    """
    Шаг №1 Выбор окружения.
    Получение списка задач по проекту.

     :return: Список InlineButtons.
    Ожидается выбор пользователя и уведомление на callback handler.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    data = await get_user_spaces(user)
    choices = tasks_click_up_keyboards.generate_inline_buttons_for_click_up_spaces(data)
    for choice in choices:
        await bot.send_message(
            message.chat.id,
            f"{choice['team_name']}",
            reply_markup=choice['keyboards']
        )

    await GetTasksByList.choose_space.set()


async def get_task_list_by_project_choose_folder(message: types.Message, state: FSMContext):
    """
    Шаг №2 Выбор папки.
    Получение списка задач по проекту.

    Функция которая вызывается из Callback Handler, get_task_list_by_project_choose_folder.
    Ожидается выбор пользователя и уведомление на callback handler.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    data = await state.get_data()

    folders = await get_user_folders_by_space_id(user, data['space_id'])

    choice = tasks_click_up_keyboards.generate_inline_buttons_for_click_up_folders(
        SpaceData(
            id=data['space_id'],
            name=data['space_name'],
            folders=folders
        )
    )

    await bot.send_message(
        message.chat.id,
        f"{data['space_name']}",
        reply_markup=choice
    )

    await GetTasksByList.choose_folder.set()


async def get_task_list_by_project_choose_list(message: types.Message, state: FSMContext):
    """
    Шаг №3 Выбор списка (bugs, backlogs, sprint) из откуда хотим взять задачи.
    Функция которая вызывается из Callback Handler, get_task_list_by_project_choose_folder

    :return: Список InlineButtons.
    Ожидается выбор пользователя и уведомление на callback handler.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    data = await state.get_data()

    folder_lists = await get_lists_by_folder(user, data['folder_id'])
    choice = tasks_click_up_keyboards.generate_inline_buttons_for_click_up_lists(folder_lists)

    await bot.send_message(message.chat.id, f"{folder_lists.name}", reply_markup=choice['keyboards'])

    await GetTasksByList.choose_list.set()


async def get_task_list_by_project_choose_task_status(message: types.Message, state: FSMContext):
    """
    Шаг №4 Выбор статуса задач (Выполненные или В работе).
    Функция которая вызывается из Callback Handler, get_task_list_by_project_choose_list

    :return: Список InlineButtons.
    Ожидается выбор пользователя и уведомление на callback handler.
    """
    choice = tasks_click_up_keyboards.generate_inline_buttons_for_click_up_task_status()

    await bot.send_message(message.chat.id, f"Выберите статус задач:", reply_markup=choice)

    await GetTasksByList.choose_task_status.set()


async def get_task_list_by_project(message: types.Message, state: FSMContext):
    """
    Шаг №5 Сбор задач.
    Функция которая вызывается из Callback Handler, get_task_list_by_project_choose_task_status

    :return: Список задач.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    data = await state.get_data()

    tasks = await get_tasks(user, data['list_id'], ClickUpTaskStatusType(data['task_group']))
    response = prepare_response_list_tasks(tasks)

    await bot.send_message(
        message.chat.id,
        f"{response}",
        parse_mode=ParseMode.HTML,
        reply_markup=tasks_click_up_keyboards.task_manager_keyboards
    )

    await state.finish()
