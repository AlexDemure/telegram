from datetime import datetime

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from src.apps.users.logic import add_new_user
from src.commands.dispatcher import dp
from src.keyboards import start_keyboards
from src.keyboards.common_keyboards import CommonKeyboards
from src.schemas.users import UserCreate


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
        reply_markup=start_keyboards.keyboards
    )


@dp.message_handler(Text(equals=[CommonKeyboards.main.value]), state=None)
async def menu(message: types.Message):
    await message.answer(
        "Вы вернулись в главное меню.\nВыберите пункт из меню.",
        parse_mode=ParseMode.HTML,
        reply_markup=start_keyboards.keyboards
    )
