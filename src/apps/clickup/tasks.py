from aiogram.types import ParseMode

from src.apps.clickup.logic import get_user_tasks, get_user_tasks_with_unset_time
from src.apps.users.logic import get_users
from src.bot.dispatcher import bot
from src.bot.messages.clickup.tasks import (
    prepare_response_list_tasks, prepare_response_list_tasks_with_unset_time
)


async def daily_send_list_tasks():
    """Ежедневная отправка задач по пользователям."""
    users = await get_users()
    for user in users:
        user_tasks = await get_user_tasks(user)
        response = prepare_response_list_tasks(user_tasks)
        await bot.send_message(user.user_id, response, parse_mode=ParseMode.HTML)


async def daily_send_list_tasks_with_unset_time():
    """Ежедневная отправка задач у которых не проставлено время выполнения."""
    users = await get_users()
    for user in users:
        user_tasks = await get_user_tasks_with_unset_time(user)
        response = prepare_response_list_tasks_with_unset_time(user_tasks)
        await bot.send_message(user.user_id, response, parse_mode=ParseMode.HTML)
