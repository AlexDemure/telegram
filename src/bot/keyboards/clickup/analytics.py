from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.keyboards.clickup.menu import MenuClickUpKeysEnum
from src.bot.keyboards.common import CommonKeysEnum


class AnalyticsClickUpKeysEnum(Enum):
    burndown_chart = "Линейная диаграмма Burndown (Для спринтов)"


keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=AnalyticsClickUpKeysEnum.burndown_chart.value),
        ],
        [
            KeyboardButton(text=MenuClickUpKeysEnum.main.value),
            KeyboardButton(text=CommonKeysEnum.main.value),
        ]
    ],
    resize_keyboard=True
)
