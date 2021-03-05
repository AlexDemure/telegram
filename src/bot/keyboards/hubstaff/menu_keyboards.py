from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.keyboards.common_keyboards import CommonKeyboards


class MenuKeyboards(Enum):
    work_log = "Журнал работ"


keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=MenuKeyboards.work_log.value),
        ],
        [
            KeyboardButton(text=CommonKeyboards.main.value),
        ]
    ],
    resize_keyboard=True
)
