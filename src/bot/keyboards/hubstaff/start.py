from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.keyboards.common import CommonKeysEnum


class StartHubStaffMenuKeysEnum(Enum):
    connect_to_hub_staff = "Подключение к HubStaff"


keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=StartHubStaffMenuKeysEnum.connect_to_hub_staff.value),
        ],
        [
            KeyboardButton(text=CommonKeysEnum.main.value),
        ]
    ],
    resize_keyboard=True
)
