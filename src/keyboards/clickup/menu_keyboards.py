from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Список задач"),
        ],
        [
            KeyboardButton(text="Задачи без запланированного времени"),
        ],
        [
            KeyboardButton(text="Учетная запись"),
        ]
    ],
    resize_keyboard=True
)
