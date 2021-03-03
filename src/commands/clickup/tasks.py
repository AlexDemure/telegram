from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from src.apps.clickup.logic import get_user_tasks, get_user_tasks_with_unset_time
from src.apps.clickup.serializer import (
    prepare_response_list_tasks, prepare_response_list_tasks_with_unset_time
)
from src.apps.users.logic import get_user, get_users
from src.commands.dispatcher import dp, bot
from src.keyboards import start_keyboards
from src.keyboards.clickup import menu_keyboards


@dp.message_handler(Text(equals=["Список задач"]), state=None)
async def get_my_tasks(message: types.Message):
    """Получение списка задач по id-пользователя из телеграмм."""
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден. Пожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    user_tasks = await get_user_tasks(user.user_id)
    response = prepare_response_list_tasks(user_tasks)

    await message.answer(f"{response}", parse_mode=ParseMode.HTML, reply_markup=menu_keyboards.keyboards)


@dp.message_handler(Text(equals=["Задачи без запланированного времени"]), state=None)
async def get_my_tasks_with_unset_time(message: types.Message):
    """Получение списка задач у которых не проставлено время выполнения."""
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден. Пожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    user_tasks = await get_user_tasks_with_unset_time(user.user_id)
    response = prepare_response_list_tasks_with_unset_time(user_tasks)

    await message.answer(f"{response}", parse_mode=ParseMode.HTML, reply_markup=menu_keyboards.keyboards)


async def daily_send_list_tasks():
    """Ежедневная отправка задач по пользователям."""
    users = await get_users()
    for user in users:
        user_tasks = await get_user_tasks(user.user_id)
        response = prepare_response_list_tasks(user_tasks)
        await bot.send_message(user.user_id, response, parse_mode=ParseMode.HTML)


async def daily_send_list_tasks_with_unset_time():
    """Ежедневная отправка задач у которых не проставлено время выполнения."""
    users = await get_users()
    for user in users:
        user_tasks = await get_user_tasks_with_unset_time(user.user_id)
        response = prepare_response_list_tasks_with_unset_time(user_tasks)
        await bot.send_message(user.user_id, response, parse_mode=ParseMode.HTML)
