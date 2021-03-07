from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from src.apps.users.logic import get_user
from src.bot.commands.dispatcher import dp
from src.bot.keyboards.clickup import menu as clickup_menu, start as clickup_start_menu
from src.bot.keyboards.hubstaff import menu as hubstaff_menu, start as hubstaff_start_menu
from src.core.enums import ServicesEnum


@dp.message_handler(
    Text(
        equals=[
            ServicesEnum.hub_staff.value,
            ServicesEnum.click_up.value
        ]
    ),
    state=None
)
async def start_menu(message: types.Message):
    """Стартовое меню со списком сервисов."""
    user = await get_user(message.chat.id)

    if message.text == ServicesEnum.hub_staff.value:
        start_menu = hubstaff_start_menu
        main_menu = hubstaff_menu
        validate_field = "hub_staff"

    elif message.text == ServicesEnum.click_up.value:
        start_menu = clickup_start_menu
        main_menu = clickup_menu
        validate_field = "click_up"

    else:
        raise ValueError

    if not user or getattr(user, validate_field, None) is None:
        response = f"Для дальнейшей работы с {message.text} необходимо подключить аккаунт."
        await message.reply(f"{response}", parse_mode=ParseMode.HTML, reply_markup=start_menu.keyboards)

    else:
        response = f"Меню {message.text}"
        await message.reply(f"{response}", parse_mode=ParseMode.HTML, reply_markup=main_menu.keyboards)


