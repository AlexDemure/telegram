from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Учетная запись HubStaff"),
        ],
    ],
    resize_keyboard=True
)
