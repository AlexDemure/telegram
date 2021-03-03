from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove, ParseMode

from src.apps.hubstaff.service import Users
from src.apps.users.logic import add_new_user, bind_hubstaff_token, get_user
from src.apps.users.schemas import UserCreate
from src.commands.dispatcher import dp, bot
from src.keyboards.hubstaff import menu_keyboards
from src.states.hubstaff_state import ConnectionHubStaffState


# URL = "https://account.hubstaff.com/authorizations/new?client_id=1PZ9zOi5sZNE6-93gHE5ZAQpXjYW9JGv4rpUIIrzVJU&response_type=code&nonce=178&redirect_uri=https://google.com&scope=openid"
# {
#     "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJqdGkiOiJRMEdOaWU4QSIsImlzcyI6Imh0dHBzOi8vYWNjb3VudC5odWJzdGFmZi5jb20iLCJleHAiOjE2MTQ4NTU5NDYsImlhdCI6MTYxNDc2OTU0Niwic2NvcGUiOiJvcGVuaWQiLCJhdWQiOiIxUFo5ek9pNXNaTkU2LTkzZ0hFNVpBUXBYallXOUpHdjRycFVJSXJ6VkpVIiwic3ViIjoicW1YVnRjYXBiVlBPdmVjZHNGT2xpaUlsVlRUNUJ4bUhZamFXYnlUbExhTWpSLURvSndXQ3QxdEQydW5MRjVKVmFheEwxYU5SYVlsWjZjU2N4MG1FbWc9PSJ9.eFkjDofpfWvjADxEqAcEViSOwagZsuGSsCXiB0EUqmzBsmTATrAfZ2Sb5CtoAhK5M9oifIquVo9RABPGyDPKTZBmVdRLFrWYLdumWGboqj1HRe6VugewIusb7lxx5Whwgf7AJcMiS9NOpOYlllx1V6YSBoJU1JRPDi5MhLOzJss1XAqej-V0UQqzxxvH10MWmxWtUIf1ib90o9YrytDP6rGdoaxS6joMvacYWZaAGXIV4h3KrZSwNqT99yHFJrOreiEbeKtVRWc1C_VyInhKA-tCwCA6ap1FgfyoK5VMsbx0BzblQ1SJKM88rgfXoS5bUn4JwOaluYYxetrxHIfi4Q",
#     "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJqdGkiOiJRMUtIenZ0NyIsImlzcyI6Imh0dHBzOi8vYWNjb3VudC5odWJzdGFmZi5jb20iLCJleHAiOjE2MTczNjE1NDYsImlhdCI6MTYxNDc2OTU0Niwic2NvcGUiOiJvcGVuaWQiLCJhdWQiOiIxUFo5ek9pNXNaTkU2LTkzZ0hFNVpBUXBYallXOUpHdjRycFVJSXJ6VkpVIiwic3ViIjoicW1YVnRjYXBiVlBPdmVjZHNGT2xpaUlsVlRUNUJ4bUhZamFXYnlUbExhTWpSLURvSndXQ3QxdEQydW5MRjVKVmFheEwxYU5SYVlsWjZjU2N4MG1FbWc9PSJ9.QLGWcuaLzWEQGmflDNLnYwUDGH97pWWq4SMwK-qCL7wIpf1QgAD3MVgyHO9XB1gHq_YyBt1uZddQ1JMUoiGByqsR4aqbFLboH4p6HU7D2GhsOF15-1cRyol4Usq2vp_NGxxPoryM2S13TClCF5ygnH9v_msN185VZOl9Ll6NB5x87QpMBfAqpKVXScEdm4Un5UnokwN4ZQTKX9X41SZ9yjNDA1uFYVPs5ZvDbriMEDS43jUY0bxv1qd_-AXn1jAgdwJfTQ08zXsCxD4d5A1dWEv1hJznrT5v-6UTaOZBIvdMsE79OHNEMFdHKBi4KI0MAdDz8oKoeZolh0kWNQ17Wg",
#     "token_type": "bearer",
#     "expires_in": 86399,
#     "id_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJpc3MiOiJodHRwczovL2FjY291bnQuaHVic3RhZmYuY29tIiwic3ViIjoicW1YVnRjYXBiVlBPdmVjZHNGT2xpaUlsVlRUNUJ4bUhZamFXYnlUbExhTWpSLURvSndXQ3QxdEQydW5MRjVKVmFheEwxYU5SYVlsWjZjU2N4MG1FbWc9PSIsImF1ZCI6IjFQWjl6T2k1c1pORTYtOTNnSEU1WkFRcFhqWVc5Skd2NHJwVUlJcnpWSlUiLCJleHAiOjE2MTQ3Njk4NDYsImlhdCI6MTYxNDc2OTU0Niwibm9uY2UiOiIyIn0.ISz0xQ9gdool9j7CXBzFMZD7LYyRrnCoIVCeTzcM7Qp8fFAE6qJzHZubuKVqpdICNN7jlUGt1lClY_YHkqnxiyKbtw1lomTg1tSGib1F-hBQCLBAlPVNc8mexoKEjeVUutzq5BtvpAGzd0QZqGya-OZ8yLICnAisIIXTp3hl4VAkKFANWNjkjSYm-v67AKJnHbcJLk9ifktSkbY4mc6wvypdrESOCfjlHLSNFaYITsyrbZSWZVIu1QEweFcHr0aPFibVoMHadnGXalR5Y04L85guPiXyedN5IWQ54VXvbgE44J-cHcS232c7XWOdY1Do8jJFeYbOu7ci51vUasvpMA"
# }

@dp.message_handler(Text(equals=["Подключение к HubStaff"]), state=None)
async def get_auth_code(message: types.Message):
    """Получение кода для возможности получить токен авторизации."""

    url = Users.get_auth_code_url()

    text = f"<i>Процесс получения кода подтверждения.</i>\n" \
           f"Для получения кода необходимо перейти по ссылке, после перехода по ссылке произойдет редирект на сайт google.com \n" \
           f"Внимательно в строке адреса сайта будет находится <u>get параметр ?code=******* необходимо скопировать и вставить</u>.\n " \
           f"<a href='{url}'>Ссылка</a>"

    await bot.send_message(message.chat.id, text, parse_mode=ParseMode.HTML)
    await bot.send_message(message.chat.id, "Введите код:", reply_markup=ReplyKeyboardRemove())

    await ConnectionHubStaffState.get_auth_token.set()


@dp.message_handler(state=ConnectionHubStaffState.get_auth_token)
async def get_auth_token(message: types.Message, state: FSMContext):
    """Получение авторизационного токена для ClickUp."""
    await state.update_data(user_id=int(message.from_user.id), hubstaff_code=message.text)
    state_data = await state.get_data()

    user = await add_new_user(UserCreate(user_id=state_data['user_id']))
    token_data = await Users.get_auth_token(state_data['hubstaff_code'])

    await bind_hubstaff_token(
        user.user_id,
        token_data['access_token'],
        token_data['refresh_token']
    )

    await message.answer(
        "Пользователь успешно добавлен.\n Выберите пункт из меню:",
        parse_mode=ParseMode.HTML,
        reply_markup=menu_keyboards.keyboards
    )
    await state.finish()


@dp.message_handler(Text(equals=["Учетная запись HubStaff"]), state=None)
async def read_user_me(message: types.Message):
    """Получение данных о пользователе из ClickUp."""
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(f"Пользователь не найден.", reply_markup=menu_keyboards.keyboards)

    user_data = await Users(f"Bearer {user.hubstaff_token}").get_user()

    await message.answer(
        f"Ваши учетные данные:\n"
        f"ID: {user_data['user']['id']}\n"
        f"EMAIL: {user_data['user']['email']}\n"
        f"USERNAME: {user_data['user']['name']}\n",
        reply_markup=menu_keyboards.keyboards
    )



