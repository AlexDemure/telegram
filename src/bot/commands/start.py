from datetime import datetime

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from src.apps.users.logic import add_new_user
from src.apps.users.schemas import UserCreate
from src.bot.dispatcher import dp
from src.bot.keyboards import start
from src.bot.keyboards.common import CommonKeysEnum


@dp.message_handler(Command('start'))
async def start_menu(message: types.Message):
    await add_new_user(
        UserCreate(
            user_id=message.from_user.id,
            registration_at=datetime.utcnow()
        )
    )

    await message.answer(
        "Добро пожаловать в Manager Bot.\nВыберите пункт из меню.",
        parse_mode=ParseMode.HTML,
        reply_markup=start.keyboards
    )


@dp.message_handler(Text(equals=[CommonKeysEnum.main.value]), state=None)
async def menu(message: types.Message):
    await message.answer(
        "Вы вернулись в главное меню.\nВыберите пункт из меню.",
        parse_mode=ParseMode.HTML,
        reply_markup=start.keyboards
    )
