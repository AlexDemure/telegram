from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove, ParseMode

from src.apps.clickup.service import ClickUp
from src.apps.users.logic import bind_click_up
from src.commands.dispatcher import dp, bot
from src.keyboards.clickup import menu_keyboards
from src.keyboards.clickup.start_keyboards import StartKeyboards
from src.schemas.clickup import ClickUpUserData
from src.states.clickup_states import ConnectionClickUpState


@dp.message_handler(Text(equals=[StartKeyboards.connect_to_click_up.value]), state=None)
async def get_auth_code(message: types.Message):
    """Получение кода для возможности получить токен авторизации."""
    text = f"<i>Процесс получения кода подтверждения.</i>\n" \
           f"Для получения кода необходимо перейти по ссылке, после перехода по ссылке произойдет редирект на сайт google.com \n" \
           f"Внимательно в строке адреса сайта будет находится <u>get параметр ?code=******* необходимо скопировать и вставить</u>.\n " \
           f"<a href='{ClickUp.get_verify_code_url()}'>Ссылка</a>"

    await bot.send_message(message.chat.id, text, parse_mode=ParseMode.HTML)
    await bot.send_message(message.chat.id, "Введите код:", reply_markup=ReplyKeyboardRemove())

    await ConnectionClickUpState.get_auth_token.set()


@dp.message_handler(state=ConnectionClickUpState.get_auth_token)
async def get_auth_token(message: types.Message, state: FSMContext):
    """Получение авторизационного токена для ClickUp."""
    #TODO Сделать через webhook
    await state.update_data(verify_code=message.text)
    state_data = await state.get_data()

    auth_token = await ClickUp.get_auth_token(state_data['verify_code'])

    click_up_user_data = await ClickUp(auth_token).get_user()

    click_up_data = ClickUpUserData(
        id=click_up_user_data['id'],
        username=click_up_user_data['username'],
        email=click_up_user_data['email'],
        auth_token=auth_token

    )
    await bind_click_up(message.chat.id, click_up_data)

    await message.answer(
        "Пользователь успешно добавлен.\nВыберите пункт из меню:",
        parse_mode=ParseMode.HTML,
        reply_markup=menu_keyboards.keyboards
    )
    await state.finish()


