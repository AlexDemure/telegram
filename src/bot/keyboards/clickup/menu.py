from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.keyboards.common import CommonKeysEnum


class MenuClickUpKeysEnum(Enum):
    me_task_menu = "Мои задачи ClickUp"
    task_manager = "Управление задачами в ClickUp"
    analytics = "Аналитика ClickUp"
    main = "В меню ClickUp"


keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=MenuClickUpKeysEnum.me_task_menu.value),
        ],
        [
            KeyboardButton(text=MenuClickUpKeysEnum.task_manager.value),
        ],
        [
            KeyboardButton(text=MenuClickUpKeysEnum.analytics.value),
        ],
        [
            KeyboardButton(text=CommonKeysEnum.main.value),
        ]
    ],
    resize_keyboard=True
)
