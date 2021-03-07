from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.keyboards.common import CommonKeysEnum


class MenuClickUpKeysEnum(Enum):
    task_list = "Список задач"
    task_list_with_unset_time = "Задачи без запланированного времени"


keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=MenuClickUpKeysEnum.task_list.value),
        ],
        [
            KeyboardButton(text=MenuClickUpKeysEnum.task_list_with_unset_time.value),
        ],
        [
            KeyboardButton(text=CommonKeysEnum.main.value),
        ]
    ],
    resize_keyboard=True
)
