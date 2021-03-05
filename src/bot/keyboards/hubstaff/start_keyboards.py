from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.keyboards.common_keyboards import CommonKeyboards


class StartKeyboards(Enum):
    connect_to_hub_staff = "Подключение к HubStaff"


keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=StartKeyboards.connect_to_hub_staff.value),
        ],
        [
            KeyboardButton(text=CommonKeyboards.main.value),
        ]
    ],
    resize_keyboard=True
)
