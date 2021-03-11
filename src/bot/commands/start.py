from datetime import datetime

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from src.apps.users.logic import add_new_user
from src.apps.users.schemas import UserCreate
from src.bot.dispatcher import dp
from src.bot.keyboards import start
from src.bot.keyboards.common import CommonKeysEnum
from src.submodules.clickup.service import ClickUp

import tempfile
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode, ReplyKeyboardRemove
import tempfile
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode, ReplyKeyboardRemove

from src.apps.clickup.logic import (
    get_user_tasks, get_user_tasks_with_unset_time, create_task,
    get_members, get_user_folders, get_lists_by_folder, get_task_by_id
)
from src.apps.users.logic import get_user
from src.bot.dispatcher import bot, dp
from src.bot.keyboards import start as start_keyboards
from src.bot.keyboards.clickup import menu as menu_click_up_keyboards
from src.bot.keyboards.clickup import tasks as tasks_click_up_keyboards
from src.bot.messages.clickup.tasks import (
    prepare_response_list_tasks, prepare_response_create_task_check_data,
    prepare_response_list_tasks_with_unset_time, prepare_response_task_data
)
from src.bot.states.clickup.tasks import CreateTaskState, GetTaskState, GetTaskListByUser
from src.submodules.clickup.enums import TagsEnumsByEmoji, PriorityEnumsByEmoji
from src.submodules.clickup.schemas import ClickUpCreateTask
from src.submodules.clickup.service import ClickUp

@dp.message_handler(Command('start'))
async def start_menu(message: types.Message):
    await add_new_user(
        UserCreate(
            user_id=message.from_user.id,
            registration_at=datetime.utcnow()
        )
    )

    await message.answer(
        "Добро пожаловать в Manager Bot.\nВыберите пункт из меню.",
        parse_mode=ParseMode.HTML,
        reply_markup=start.keyboards
    )


@dp.message_handler(content_types=['photo', 'document'])
async def start_menu(message: types.Message):

    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    data_string_with_file_in_bytes()
    data_string_with_file_in_buffered()
    data_string_with_file_in_base64_bytes()
    data_string_with_file_in_base64_string()

    data_dictionary_with_file_in_bytes()
    data_dictionary_with_file_in_buffered()
    data_dictionary_with_file_in_base64_bytes()
    data_dictionary_with_file_in_base64_string()

import requests

headers = {
    'Authorization': "6655746_f2d0df7798fd0e1952c7a4123ba2fc00eaf354c3",
    'Content-Type': 'multipart/form-data',
}
url = "https://api.clickup.com/api/v2/task/f0zn4t/attachment"

test_file = open('test.png', 'rb')
data = 'attachment: raw_image_file (file) filename: example.png (string)'


def data_string_with_file_in_bytes():
    data = f"attachment: {test_file.read()} filename: test.png"
    response = requests.post(url, headers=headers, data=data)
    print("String data [file in bytes]", response.status_code, response.json())


def data_string_with_file_in_buffered():
    data = f"attachment: {test_file} filename: test.png"
    response = requests.post(url, headers=headers, data=data)
    print("String data [file in buffered]", response.status_code, response.json())


def data_string_with_file_in_base64_bytes():
    import base64
    data = f"attachment: {base64.b64encode(test_file.read())} filename: test.png"
    response = requests.post(url, headers=headers, data=data)
    print("String data [file in base64 bytes]", response.status_code, response.json())


def data_string_with_file_in_base64_string():
    import base64
    data = f"attachment: {base64.b64decode(base64.b64encode(test_file.read()))} filename: test.png"
    response = requests.post(url, headers=headers, data=data)
    print("String data [file in base64 string]", response.status_code, response.json())


def data_dictionary_with_file_in_bytes():
    data = dict(
        attachment=test_file.read(),
        filename="test.png"
    )
    response = requests.post(url, headers=headers, data=data)
    print("Dict data with params data [file in bytes]", response.status_code, response.json())

    response = requests.post(url, headers=headers, files=data)
    print("Dict data with params files [file in bytes]", response.status_code, response.json())


def data_dictionary_with_file_in_buffered():
    data = dict(
        attachment=test_file,
        filename="test.png"
    )
    response = requests.post(url, headers=headers, data=data)
    print("Dict data with params data [file in buffered]", response.status_code, response.json())

    response = requests.post(url, headers=headers, files=data)
    print("Dict data with params files [file in buffered]", response.status_code, response.json())


def data_dictionary_with_file_in_base64_bytes():
    import base64

    data = dict(
        attachment=base64.b64encode(test_file.read()),
        filename="test.png"
    )
    response = requests.post(url, headers=headers, data=data)
    print("Dict data with params data [file in base64 bytes]", response.status_code, response.json())

    response = requests.post(url, headers=headers, data=data)
    print("Dict data with params files [file in base64 bytes]", response.status_code, response.json())


def data_dictionary_with_file_in_base64_string():
    import base64

    data = dict(
        attachment=base64.b64decode(base64.b64encode(test_file.read())),
        filename="test.png"
    )
    response = requests.post(url, headers=headers, data=data)
    print("Dict data with params data [file in base64 string]", response.status_code, response.json())

    response = requests.post(url, headers=headers, files=data)
    print("Dict data with params files [file in base64 string]", response.status_code, response.json())


@dp.message_handler(Text(equals=[CommonKeysEnum.main.value]), state=None)
async def menu(message: types.Message):
    await message.answer(
        "Вы вернулись в главное меню.\nВыберите пункт из меню.",
        parse_mode=ParseMode.HTML,
        reply_markup=start.keyboards
    )
