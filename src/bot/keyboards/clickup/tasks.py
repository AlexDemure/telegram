import logging
from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from src.bot.keyboards.clickup.menu import MenuClickUpKeysEnum
from src.bot.keyboards.common import CommonKeysEnum
from src.submodules.clickup.enums import Teams, ClickUpTaskStatusType
from src.submodules.clickup.schemas import ClickUpData, FolderData, UserGroups, SpaceData


class TaskManagerClickUpKeysEnum(Enum):
    create_task = "Создать задачу"
    get_task = "Поиск задачи"
    task_list_by_user = "Список задач по пользователю"
    task_list_by_project = "Список задач по проекту"


task_manager_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=TaskManagerClickUpKeysEnum.task_list_by_project.value),
        ],
        [
            KeyboardButton(text=TaskManagerClickUpKeysEnum.task_list_by_user.value),
        ],
        [
            KeyboardButton(text=TaskManagerClickUpKeysEnum.create_task.value),
            KeyboardButton(text=TaskManagerClickUpKeysEnum.get_task.value),
        ],
        [
            KeyboardButton(text=MenuClickUpKeysEnum.main.value),
            KeyboardButton(text=CommonKeysEnum.main.value),
        ]
    ],
    resize_keyboard=True
)


class MeMenuClickUpKeysEnum(Enum):
    task_list = "Список моих задач"
    task_list_with_unset_time = "Список моих задач без времени"


me_menu_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=MeMenuClickUpKeysEnum.task_list.value),
        ],
        [
            KeyboardButton(text=MeMenuClickUpKeysEnum.task_list_with_unset_time.value),
        ],
        [
            KeyboardButton(text=MenuClickUpKeysEnum.main.value),
            KeyboardButton(text=CommonKeysEnum.main.value),
        ]
    ],
    resize_keyboard=True
)


def generate_inline_buttons_for_click_up_spaces(data: ClickUpData) -> list:
    choices = []
    for team in data.teams:
        choice = InlineKeyboardMarkup(row_width=1)
        for space in team.spaces:
            try:
                choice.insert(
                    InlineKeyboardButton(
                        text=space.name[:128],
                        callback_data=CallbackData("spaces", "id", "name").new(
                            id=space.id,
                            name=space.name[:128]
                        )
                    )
                )
            except Exception:
                logging.error(f"Callback is wrong:{space.dict()}")
                continue

        choices.append(dict(team_name=team.name, keyboards=choice))

    return choices


def generate_inline_buttons_for_click_up_folders(data: SpaceData) -> InlineKeyboardMarkup:
    choice = InlineKeyboardMarkup(row_width=1)
    for folder in data.folders:
        choice.insert(
            InlineKeyboardButton(
                text=folder.name[:128],
                callback_data=CallbackData("folders", "id", "name").new(
                    id=folder.id,
                    name=folder.name[:128]
                )
            )
        )

    return choice


def generate_inline_buttons_for_click_up_lists(folder: FolderData) -> dict:
    choice = InlineKeyboardMarkup(row_width=3)
    for folder_list in folder.lists:
        choice.insert(
            InlineKeyboardButton(
                text=folder_list.name,
                callback_data=CallbackData("lists", "id", "name").new(
                    id=folder_list.id,
                    name=folder_list.name
                )
            )
        )

    return dict(folder_name=folder.name, keyboards=choice)


def generate_inline_buttons_for_click_up_members(members: UserGroups) -> list:
    choices = []

    for group, values in members.dict().items():
        choice = InlineKeyboardMarkup(row_width=2)

        for member in values:
            choice.insert(
                InlineKeyboardButton(
                    text=member['username'],
                    callback_data=CallbackData("assigned", "id", "username").new(
                        id=member['id'],
                        username=member['username']
                    )
                )
            )
        preview_name = getattr(Teams, group).preview_name if getattr(Teams, group) else "Неизвестно"
        choices.append(dict(member_group=preview_name, keyboards=choice))

    return choices


def generate_inline_buttons_for_click_up_tags(tags: list) -> dict:
    choice = InlineKeyboardMarkup(row_width=1)

    for tag in tags:
        choice.insert(
            InlineKeyboardButton(
                text=tag[1],
                callback_data=CallbackData("tags", "name").new(name=tag[0])
            )
        )

    return dict(response="Список тегов (Выбор нескольких вариантов):", keyboards=choice)


def generate_inline_buttons_for_click_up_priority(priorities: list) -> dict:
    choice = InlineKeyboardMarkup(row_width=1)

    for priority in priorities:
        choice.insert(
            InlineKeyboardButton(
                text=priority[1],
                callback_data=CallbackData("priorities", "name").new(name=priority[0])
            )
        )

    return dict(response="Список приоритетов:", keyboards=choice)


def generate_inline_buttons_for_click_up_check_data() -> InlineKeyboardMarkup:
    choice = InlineKeyboardMarkup(row_width=1)

    choice.insert(
        InlineKeyboardButton(
            text="Создать",
            callback_data=CallbackData("create_task", "action").new(action="Создать")
        )
    )
    choice.insert(
        InlineKeyboardButton(
            text="Отменить",
            callback_data=CallbackData("create_task", "action").new(action="Отменить")
        )
    )

    return choice


def generate_inline_buttons_for_click_up_task_status() -> InlineKeyboardMarkup:
    choice = InlineKeyboardMarkup(row_width=3)

    for x in ClickUpTaskStatusType:
        choice.insert(
            InlineKeyboardButton(
                text=x.preview_name,
                callback_data=CallbackData("task_status", "task_group").new(task_group=x.value)
            )
        )

    return choice


def generate_inline_buttons_for_click_up_task_control(is_new_task: bool = False) -> InlineKeyboardMarkup:
    choice = InlineKeyboardMarkup(row_width=1)

    choice.insert(
        InlineKeyboardButton(
            text="Добавить файл",
            callback_data=CallbackData("task_control", "action").new(action="add_file")
        )
    )

    choice.insert(
        InlineKeyboardButton(
            text="Добавить комментарий",
            callback_data=CallbackData("task_control", "action").new(action="add_comment")
        )
    )
    if is_new_task is False:
        choice.insert(
            InlineKeyboardButton(
                text="Список комментариев",
                callback_data=CallbackData("task_control", "action").new(action="list_comment")
            )
        )

    choice.insert(
        InlineKeyboardButton(
            text="Выход",
            callback_data=CallbackData("task_control", "action").new(action="cancel")
        )
    )

    return choice


def generate_inline_buttons_for_click_up_add_files() -> InlineKeyboardMarkup:
    choice = InlineKeyboardMarkup(row_width=1)

    choice.insert(
        InlineKeyboardButton(
            text="Добавить еще",
            callback_data=CallbackData("task_control", "action").new(action="add_file")
        )
    )

    choice.insert(
        InlineKeyboardButton(
            text="Выход",
            callback_data=CallbackData("task_control", "action").new(action="cancel")
        )
    )

    return choice
