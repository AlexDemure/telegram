from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.keyboards.common import CommonKeysEnum


class MenuOtherKeysEnum(Enum):
    it_jokes = "Айтишные фразы"
    evil_insult = "Получить оскорбление"


menu_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=MenuOtherKeysEnum.it_jokes.value),
        ],
        [
            KeyboardButton(text=MenuOtherKeysEnum.evil_insult.value),
        ],
        [
            KeyboardButton(text=CommonKeysEnum.main.value),
        ]
    ],
    resize_keyboard=True
)
