from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.keyboards.common import CommonKeysEnum


class WorkLogHubStaffKeysEnum(Enum):
    work_log_today = "Журнал работ за сегодня"
    work_log_yesterday = "Журнал работ за предыдущий день"
    work_log_week = "Журнал работ за неделю"


keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=WorkLogHubStaffKeysEnum.work_log_today.value),
        ],
        [
            KeyboardButton(text=WorkLogHubStaffKeysEnum.work_log_yesterday.value),
        ],
        [
            KeyboardButton(text=WorkLogHubStaffKeysEnum.work_log_week.value),
        ],
        [
            KeyboardButton(text=CommonKeysEnum.main.value),
        ]
    ],
    resize_keyboard=True
)