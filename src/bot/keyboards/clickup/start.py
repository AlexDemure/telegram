from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.keyboards.common import CommonKeysEnum


class StartClickUpMenuKeysEnum(Enum):
    connect_to_click_up = "Подключение к ClickUp"


keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=StartClickUpMenuKeysEnum.connect_to_click_up.value),
        ],
        [
            KeyboardButton(text=CommonKeysEnum.main.value),
        ]
    ],
    resize_keyboard=True
)
