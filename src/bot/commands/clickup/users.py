from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove, ParseMode

from src.apps.clickup.logic import add_click_up_data_by_user
from src.bot.commands.dispatcher import dp, bot
from src.bot.keyboards.clickup import menu_keyboards
from src.bot.keyboards.clickup.start_keyboards import StartKeyboards
from src.bot.states.clickup_states import ConnectionClickUpState
from src.bot.messages.oauth_code import prepare_response_get_verify_code
from src.submodules.clickup.service import ClickUpOAuth


@dp.message_handler(Text(equals=[StartKeyboards.connect_to_click_up.value]), state=None)
async def get_auth_code(message: types.Message):
    """Получение кода для возможности получить токен авторизации."""
    response = prepare_response_get_verify_code(ClickUpOAuth.get_verify_code_url())

    await bot.send_message(message.chat.id, response, parse_mode=ParseMode.HTML)
    await bot.send_message(message.chat.id, "Введите код:", reply_markup=ReplyKeyboardRemove())

    await ConnectionClickUpState.add_click_up_data.set()


@dp.message_handler(state=ConnectionClickUpState.add_click_up_data)
async def add_click_up_data(message: types.Message, state: FSMContext):
    """Получение авторизационного токена для ClickUp."""
    #TODO Сделать через webhook

    await state.update_data(verify_code=message.text)
    state_data = await state.get_data()

    await add_click_up_data_by_user(message.chat.id, state_data['verify_code'])

    await message.answer(
        "Пользователь успешно добавлен.\nВыберите пункт из меню:",
        parse_mode=ParseMode.HTML,
        reply_markup=menu_keyboards.keyboards
    )
    await state.finish()


