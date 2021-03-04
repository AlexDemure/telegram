from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.keyboards.common_keyboards import CommonKeyboards


class MenuKeyboards(Enum):
    task_list = "Список задач"
    task_list_with_unset_time = "Задачи без запланированного времени"


keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=MenuKeyboards.task_list.value),
        ],
        [
            KeyboardButton(text=MenuKeyboards.task_list_with_unset_time.value),
        ],
        [
            KeyboardButton(text=CommonKeyboards.main.value),
        ]
    ],
    resize_keyboard=True
)
