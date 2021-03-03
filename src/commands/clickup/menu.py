from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from src.apps.users.logic import get_user
from src.commands.dispatcher import dp
from src.keyboards.clickup import menu_keyboards, start_keyboards


@dp.message_handler(Text(equals=["ClickUp"]), state=None)
async def start_menu(message: types.Message):
    """Стартовое меню ClickUp."""
    user = await get_user(message.chat.id)
    if not user or not user.clickup_token:
        response = f"Для дальнейшей работы с ClickUp необходимо подключить аккаунт."
        await message.reply(f"{response}", parse_mode=ParseMode.HTML, reply_markup=start_keyboards.keyboards)
    else:
        response = f"<b>Меню ClickUp</b>"
        await message.reply(f"{response}", parse_mode=ParseMode.HTML, reply_markup=menu_keyboards.keyboards)

