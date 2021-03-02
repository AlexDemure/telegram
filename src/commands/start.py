from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode

from src.commands.dispatcher import dp
from src.keyboards import start_keyboards


@dp.message_handler(Command('start'))
async def start_menu(message: types.Message):
    await message.answer(
        f"<b>Добро пожаловать в Manager Bot.</b>\nВыберите пункт из меню:",
        parse_mode=ParseMode.HTML,
        reply_markup=start_keyboards.keyboards
    )
