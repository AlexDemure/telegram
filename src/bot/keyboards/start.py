from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.core.enums import ServicesEnum


class MainMenuKeysEnum(Enum):
    other = 'Развлечения'


keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=ServicesEnum.click_up.value),
        ],
        [
            KeyboardButton(text=ServicesEnum.hub_staff.value),
        ],
        [
            KeyboardButton(text=MainMenuKeysEnum.other.value),
        ],
    ],
    resize_keyboard=True
)
