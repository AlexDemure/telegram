from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Подключение к ClickUp"),
        ]
    ],
    resize_keyboard=True
)
