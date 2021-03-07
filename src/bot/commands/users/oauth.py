from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode, ReplyKeyboardRemove

from src.bot.commands.dispatcher import dp, bot
from src.bot.keyboards.clickup.start import StartClickUpMenuKeysEnum
from src.bot.keyboards.hubstaff.start import StartHubStaffMenuKeysEnum
from src.bot.messages.users.oauth import prepare_response_get_verify_code
from src.core.enums import ServicesEnum
from src.core.urls import get_webhook_url, OAUTH_ENDPOINT
from src.submodules.clickup.service import ClickUpOAuth
from src.submodules.hubstaff.service import HubStaffOAuth
from src.utils import encode_data_to_base64


@dp.message_handler(
    Text(
        equals=[
            StartClickUpMenuKeysEnum.connect_to_click_up.value,
            StartHubStaffMenuKeysEnum.connect_to_hub_staff.value
        ]
    ),
    state=None
)
async def get_auth_code(message: types.Message):
    """Получение кода для возможности получить токен авторизации."""
    redirect_uri = f"{get_webhook_url(OAUTH_ENDPOINT, short_url=False)}"

    if message.text == StartClickUpMenuKeysEnum.connect_to_click_up.value:
        url = ClickUpOAuth.get_verify_code_url(
            redirect_uri=redirect_uri,
            state=encode_data_to_base64(dict(system=ServicesEnum.click_up.value, user_id=message.chat.id))
        )
    elif message.text == StartHubStaffMenuKeysEnum.connect_to_hub_staff.value:
        url = HubStaffOAuth.get_verify_code_url(
            redirect_uri=redirect_uri,
            state=encode_data_to_base64(dict(system=ServicesEnum.hub_staff.value, user_id=message.chat.id))
        )
    else:
        raise ValueError

    response = prepare_response_get_verify_code(url)

    await bot.send_message(message.chat.id, response, parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
