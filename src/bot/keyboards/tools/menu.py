from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.keyboards.common import CommonKeysEnum


class MenuToolsKeysEnum(Enum):
    pert = "Оценка сроков (PERT)"


menu_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=MenuToolsKeysEnum.pert.value),
        ],
        [
            KeyboardButton(text=CommonKeysEnum.main.value),
        ]
    ],
    resize_keyboard=True
)
