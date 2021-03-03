from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Подключение к HubStaff"),
        ],
    ],
    resize_keyboard=True
)
