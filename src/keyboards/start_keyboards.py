from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class StartKeyboards(Enum):
    click_up = "ClickUp"
    hub_staff = "HubStaff"


keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=StartKeyboards.click_up.value),
        ],
        [
            KeyboardButton(text=StartKeyboards.hub_staff.value),
        ]
    ],
    resize_keyboard=True
)
