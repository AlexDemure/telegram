from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.keyboards.common_keyboards import CommonKeyboards


class WorkLogKeyboards(Enum):
    work_log_today = "Журнал работ за сегодня"
    work_log_yesterday = "Журнал работ за предыдущий день"
    work_log_week = "Журнал работ за неделю"


keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=WorkLogKeyboards.work_log_today.value),
        ],
        [
            KeyboardButton(text=WorkLogKeyboards.work_log_yesterday.value),
        ],
        [
            KeyboardButton(text=WorkLogKeyboards.work_log_week.value),
        ],
        [
            KeyboardButton(text=CommonKeyboards.main.value),
        ]
    ],
    resize_keyboard=True
)