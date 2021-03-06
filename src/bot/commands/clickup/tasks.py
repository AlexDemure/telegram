from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from src.apps.clickup.logic import get_user_tasks, get_user_tasks_with_unset_time
from src.apps.users.logic import get_user
from src.bot.commands.dispatcher import dp
from src.bot.keyboards import start_keyboards
from src.bot.keyboards.clickup import menu_keyboards
from src.bot.keyboards.clickup.menu_keyboards import MenuKeyboards
from src.bot.messages.clickup.tasks import (
    prepare_response_list_tasks, prepare_response_list_tasks_with_unset_time
)


@dp.message_handler(Text(equals=[MenuKeyboards.task_list.value]), state=None)
async def get_my_tasks(message: types.Message):
    """Получение списка задач по id-пользователя из телеграмм."""
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    user_tasks = await get_user_tasks(user)
    response = prepare_response_list_tasks(user_tasks)

    await message.answer(f"{response}", parse_mode=ParseMode.HTML, reply_markup=menu_keyboards.keyboards)


@dp.message_handler(Text(equals=[MenuKeyboards.task_list_with_unset_time.value]), state=None)
async def get_my_tasks_with_unset_time(message: types.Message):
    """Получение списка задач у которых не проставлено время выполнения."""
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден. Пожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    user_tasks = await get_user_tasks_with_unset_time(user)
    response = prepare_response_list_tasks_with_unset_time(user_tasks)

    await message.answer(f"{response}", parse_mode=ParseMode.HTML, reply_markup=menu_keyboards.keyboards)


