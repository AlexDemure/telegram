from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from src.apps.users.logic import get_user
from src.commands.dispatcher import dp
from src.keyboards.hubstaff import menu_keyboards, start_keyboards


@dp.message_handler(Text(equals=["HubStaff"]), state=None)
async def start_menu(message: types.Message):
    """Стартовое меню Hubstaff."""
    user = await get_user(message.chat.id)
    if not user or not user.hubstaff_token:
        response = f"Для дальнейшей работы с HubStaff необходимо подключить аккаунт."
        await message.reply(f"{response}", parse_mode=ParseMode.HTML, reply_markup=start_keyboards.keyboards)
    else:
        response = f"<b>Меню HubStaff</b>"
        await message.reply(f"{response}", parse_mode=ParseMode.HTML, reply_markup=menu_keyboards.keyboards)
