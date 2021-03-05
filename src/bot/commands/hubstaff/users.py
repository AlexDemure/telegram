from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove, ParseMode

from src.apps.hubstaff.logic import add_hub_staff_data_by_user
from src.bot.commands.dispatcher import dp, bot
from src.bot.keyboards.hubstaff import menu_keyboards
from src.bot.keyboards.hubstaff.start_keyboards import StartKeyboards
from src.bot.messages.oauth_code import prepare_response_get_verify_code
from src.bot.states.hubstaff_states import ConnectionHubStaffState
from src.submodules.hubstaff.service import HubStaffOAuth


@dp.message_handler(Text(equals=[StartKeyboards.connect_to_hub_staff.value]), state=None)
async def get_auth_code(message: types.Message):
    """Получение кода для возможности получить токен авторизации."""
    response = prepare_response_get_verify_code(HubStaffOAuth.get_verify_code_url())

    await bot.send_message(message.chat.id, response, parse_mode=ParseMode.HTML)
    await bot.send_message(message.chat.id, "Введите код:", reply_markup=ReplyKeyboardRemove())

    await ConnectionHubStaffState.add_hub_staff_data.set()


@dp.message_handler(state=ConnectionHubStaffState.add_hub_staff_data)
async def get_auth_token(message: types.Message, state: FSMContext):
    """Получение авторизационного токена для HubStaff."""
    await state.update_data(verify_code=message.text)
    state_data = await state.get_data()

    await add_hub_staff_data_by_user(message.chat.id, state_data['verify_code'])

    await message.answer(
        "Пользователь успешно добавлен.\nВыберите пункт из меню:",
        parse_mode=ParseMode.HTML,
        reply_markup=menu_keyboards.keyboards
    )
    await state.finish()
