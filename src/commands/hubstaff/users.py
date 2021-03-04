from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove, ParseMode

from src.apps.hubstaff.service import HubStaff
from src.apps.users.logic import bind_hub_staff, get_user
from src.commands.dispatcher import dp, bot
from src.keyboards.hubstaff import menu_keyboards
from src.keyboards.hubstaff.start_keyboards import StartKeyboards
from src.schemas.hubstaff import HubStaffUserData
from src.states.hubstaff_states import ConnectionHubStaffState


@dp.message_handler(Text(equals=[StartKeyboards.connect_to_hub_staff.value]), state=None)
async def get_auth_code(message: types.Message):
    """Получение кода для возможности получить токен авторизации."""
    text = f"<i>Процесс получения кода подтверждения.</i>\n" \
           f"Для получения кода необходимо перейти по ссылке, после перехода по ссылке произойдет редирект на сайт google.com \n" \
           f"Внимательно в строке адреса сайта будет находится <u>get параметр ?code=******* необходимо скопировать и вставить</u>.\n " \
           f"<a href='{HubStaff.get_verify_code_url()}'>Ссылка</a>"

    await bot.send_message(message.chat.id, text, parse_mode=ParseMode.HTML)
    await bot.send_message(message.chat.id, "Введите код:", reply_markup=ReplyKeyboardRemove())

    await ConnectionHubStaffState.get_auth_token.set()


@dp.message_handler(state=ConnectionHubStaffState.get_auth_token)
async def get_auth_token(message: types.Message, state: FSMContext):
    """Получение авторизационного токена для HubStaff."""
    await state.update_data(verify_code=message.text)
    state_data = await state.get_data()

    token_data = await HubStaff.get_auth_token(state_data['verify_code'])

    hub_staff_user_data = await HubStaff(f"Bearer {token_data['access_token']}").get_user()

    hub_staff_data = HubStaffUserData(
        id=hub_staff_user_data['id'],
        username=hub_staff_user_data['name'],
        email=hub_staff_user_data['email'],
        auth_token=f"Bearer {token_data['access_token']}",
        refresh_token=token_data['refresh_token']
    )
    await bind_hub_staff(message.chat.id, hub_staff_data)

    await message.answer(
        "Пользователь успешно добавлен.\nВыберите пункт из меню:",
        parse_mode=ParseMode.HTML,
        reply_markup=menu_keyboards.keyboards
    )
    await state.finish()
