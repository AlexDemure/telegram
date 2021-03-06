from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode, ReplyKeyboardRemove

from src.bot.commands.dispatcher import dp, bot
from src.bot.keyboards.clickup.start_keyboards import StartKeyboards
from src.bot.messages.oauth_code import prepare_response_get_verify_code
from src.core.config import settings
from src.submodules.clickup.service import ClickUpOAuth
from src.utils import encode_data_to_base64


@dp.message_handler(Text(equals=[StartKeyboards.connect_to_click_up.value]), state=None)
async def get_auth_code(message: types.Message):
    """Получение кода для возможности получить токен авторизации."""
    response = prepare_response_get_verify_code(
        ClickUpOAuth.get_verify_code_url(
            redirect_uri=f"{settings.webhook_uri}/connect",
            state=encode_data_to_base64(dict(system="clickup", user_id=message.chat.id))
        )
    )

    await bot.send_message(message.chat.id, response, parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
