from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove, ParseMode

from src.apps.clickup.service import ClickUp
from src.apps.users.logic import add_new_user, get_user, bind_clickup_token
from src.apps.users.schemas import UserCreate
from src.commands.dispatcher import dp, bot
from src.core.config import settings
from src.keyboards.clickup import menu_keyboards
from src.states.clickup_state import ConnectionClickUpState


@dp.message_handler(Text(equals=["Подключение к ClickUp"]), state=None)
async def get_auth_code(message: types.Message):
    """Получение кода для возможности получить токен авторизации."""
    text = f"<i>Процесс получения кода подтверждения.</i>\n" \
           f"Для получения кода необходимо перейти по ссылке, после перехода по ссылке произойдет редирект на сайт google.com \n" \
           f"Внимательно в строке адреса сайта будет находится <u>get параметр ?code=******* необходимо скопировать и вставить</u>.\n " \
           f"<a href='https://app.clickup.com/api?client_id={settings.CLICKUP_CLIENT_ID}&redirect_uri=https://google.com'>Ссылка</a>"

    await bot.send_message(message.chat.id, text, parse_mode=ParseMode.HTML)
    await bot.send_message(message.chat.id, "Введите код:", reply_markup=ReplyKeyboardRemove())

    await ConnectionClickUpState.get_auth_token.set()


@dp.message_handler(state=ConnectionClickUpState.get_auth_token)
async def get_auth_token(message: types.Message, state: FSMContext):
    """Получение авторизационного токена для ClickUp."""
    await state.update_data(user_id=int(message.from_user.id), click_code=message.text)
    state_data = await state.get_data()

    user = await add_new_user(
        UserCreate(user_id=state_data['user_id'])
    )

    auth_token = await ClickUp.get_auth_token(state_data['click_code'])

    await bind_clickup_token(user.user_id, auth_token['access_token'])

    await message.answer(
        "Пользователь успешно добавлен.\n Выберите пункт из меню:",
        parse_mode=ParseMode.HTML,
        reply_markup=menu_keyboards.keyboards
    )
    await state.finish()


@dp.message_handler(Text(equals=["Учетная запись"]), state=None)
async def read_user_me(message: types.Message):
    """Получение данных о пользователе из ClickUp."""
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(f"Пользователь не найден.", reply_markup=menu_keyboards.keyboards)

    user_data = await ClickUp(user.clickup_token).get_user()
    await message.answer(
        f"Ваши учетные данные:\n"
        f"ID: {user_data.id}\n"
        f"EMAIL: {user_data.email}\n"
        f"USERNAME: {user_data.username}\n",
        reply_markup=menu_keyboards.keyboards
    )



