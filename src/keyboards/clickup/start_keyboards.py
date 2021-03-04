from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.keyboards.common_keyboards import CommonKeyboards


class StartKeyboards(Enum):
    connect_to_click_up = "Подключение к ClickUp"


keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=StartKeyboards.connect_to_click_up.value),
        ],
        [
            KeyboardButton(text=CommonKeyboards.main.value),
        ]
    ],
    resize_keyboard=True
)
