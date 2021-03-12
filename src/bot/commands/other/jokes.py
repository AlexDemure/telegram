from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from google_trans_new import google_translator

from src.bot.dispatcher import dp
from src.bot.keyboards.other.menu import MenuOtherKeysEnum, menu_keyboards
from src.bot.keyboards.start import MainMenuKeysEnum
from src.submodules.common.base_class import APIClass

api = APIClass()
translator = google_translator()


@dp.message_handler(Text(equals=[MainMenuKeysEnum.other.value]), state=None)
async def start_other_menu(message: types.Message):
    """
    Главное меню с Разными функциями.
    :return: Клавиатуру с выбором "Разных функций" (Айти фразы, оскорбления)
    """
    await message.answer(
        f"Меню с разными функциями:",
        parse_mode=ParseMode.HTML,
        reply_markup=menu_keyboards
    )


@dp.message_handler(Text(equals=[MenuOtherKeysEnum.it_jokes.value]), state=None)
async def get_it_joke(message: types.Message):
    """
    Handler по нажатию Кнопки "Айти фразы".

    :return: Айтишная фраза
    """
    data = await api.make_request("GET", "https://v2.jokeapi.dev/joke/Programming?type=single")

    response = f"{translator.translate(data['joke'], lang_tgt='ru')}\n\n" \
               f"<i>Original: {data['joke']}</i>"

    await message.answer(
        response,
        parse_mode=ParseMode.HTML,
        reply_markup=menu_keyboards
    )


@dp.message_handler(Text(equals=[MenuOtherKeysEnum.evil_insult.value]), state=None)
async def get_evil_insult(message: types.Message):
    """
    Handler по нажатию Кнопки "Айти фразы".

    :return: Айтишная фраза
    """
    data = await api.make_request("GET", "https://evilinsult.com/generate_insult.php?lang=en&type=json")

    response = f"{translator.translate(data['insult'], lang_tgt='ru')}\n\n" \
               f"<i>Original: {data['insult']}</i>"

    await message.answer(
        response,
        parse_mode=ParseMode.HTML,
        reply_markup=menu_keyboards
    )
