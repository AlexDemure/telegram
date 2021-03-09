from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from src.apps.hubstaff.logic import get_activities_by_period
from src.apps.users.logic import get_user
from src.bot.dispatcher import dp, bot
from src.bot.keyboards.hubstaff import menu, activities
from src.bot.keyboards.hubstaff.activities import WorkLogHubStaffKeysEnum
from src.bot.keyboards.hubstaff.menu import MenuHubStaffKeysEnum
from src.bot.messages.hubstaff.activities import prepare_response_activities_list


@dp.message_handler(Text(equals=[MenuHubStaffKeysEnum.work_log.value]), state=None)
async def get_activity(message: types.Message):
    await bot.send_message(message.chat.id, "Выберите период:", reply_markup=activities.keyboards)


@dp.message_handler(Text(equals=[WorkLogHubStaffKeysEnum.work_log_today.value]), state=None)
async def get_activity_today(message: types.Message):
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(f"Пользователь не найден.", reply_markup=menu.keyboards)

    start_date = end_date = datetime.utcnow()

    reports = await get_activities_by_period(user, start_date, end_date)
    response = prepare_response_activities_list(reports)

    await message.answer(f"{response}", parse_mode=ParseMode.HTML, reply_markup=activities.keyboards)


@dp.message_handler(Text(equals=[WorkLogHubStaffKeysEnum.work_log_yesterday.value]), state=None)
async def get_activity_yesterday(message: types.Message):
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(f"Пользователь не найден.", reply_markup=menu.keyboards)

    start_date = end_date = datetime.utcnow() - timedelta(days=1)

    reports = await get_activities_by_period(user, start_date, end_date)
    response = prepare_response_activities_list(reports)

    await message.answer(f"{response}", parse_mode=ParseMode.HTML, reply_markup=activities.keyboards)


@dp.message_handler(Text(equals=[WorkLogHubStaffKeysEnum.work_log_week.value]), state=None)
async def get_activity_week(message: types.Message):
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(f"Пользователь не найден.", reply_markup=menu.keyboards)

    start_date = datetime.utcnow() - timedelta(days=7)
    end_date = datetime.utcnow()

    reports = await get_activities_by_period(user, start_date, end_date)
    response = prepare_response_activities_list(reports)

    await message.answer(f"{response}", parse_mode=ParseMode.HTML, reply_markup=activities.keyboards)


