from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="ClickUp"),
            KeyboardButton(text="HubStaff"),
        ]
    ],
    resize_keyboard=True
)
