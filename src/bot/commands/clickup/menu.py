from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from src.apps.users.logic import get_user
from src.bot.commands.dispatcher import dp
from src.bot.keyboards.clickup import menu_keyboards, start_keyboards
from src.bot.keyboards.start_keyboards import StartKeyboards


@dp.message_handler(Text(equals=[StartKeyboards.click_up.value]), state=None)
async def start_menu(message: types.Message):
    """Стартовое меню ClickUp."""
    user = await get_user(message.chat.id)

    if not user or not user.click_up:
        response = f"Для дальнейшей работы с ClickUp необходимо подключить аккаунт."
        await message.reply(f"{response}", parse_mode=ParseMode.HTML, reply_markup=start_keyboards.keyboards)

    else:
        response = f"Меню ClickUp"
        await message.reply(f"{response}", parse_mode=ParseMode.HTML, reply_markup=menu_keyboards.keyboards)


