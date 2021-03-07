from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.keyboards.common import CommonKeysEnum


class MenuHubStaffKeysEnum(Enum):
    work_log = "Журнал работ"


keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=MenuHubStaffKeysEnum.work_log.value),
        ],
        [
            KeyboardButton(text=CommonKeysEnum.main.value),
        ]
    ],
    resize_keyboard=True
)
