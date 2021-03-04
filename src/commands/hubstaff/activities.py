from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from src.apps.hubstaff.service import HubStaff
from src.apps.users.logic import get_user
from src.commands.dispatcher import dp, bot
from src.keyboards.hubstaff import menu_keyboards, activities_keyboards
from src.keyboards.hubstaff.activities_keyboards import WorkLogKeyboards
from src.keyboards.hubstaff.menu_keyboards import MenuKeyboards
from src.messages.hubstaff.activities import prepare_response_activities_list


@dp.message_handler(Text(equals=[MenuKeyboards.work_log.value]), state=None)
async def get_activity(message: types.Message):
    await bot.send_message(message.chat.id, "Выберите период:", reply_markup=activities_keyboards.keyboards)


@dp.message_handler(Text(equals=[WorkLogKeyboards.work_log_today.value]), state=None)
async def get_activity_today(message: types.Message):
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(f"Пользователь не найден.", reply_markup=menu_keyboards.keyboards)

    date_today = datetime.utcnow()

    reports = await HubStaff(user.hub_staff.auth_token).collect_user_activities_by_period(date_today, date_today)

    response = prepare_response_activities_list(reports)
    await message.answer(f"{response}", parse_mode=ParseMode.HTML, reply_markup=activities_keyboards.keyboards)


@dp.message_handler(Text(equals=[WorkLogKeyboards.work_log_yesterday.value]), state=None)
async def get_activity_yesterday(message: types.Message):
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(f"Пользователь не найден.", reply_markup=menu_keyboards.keyboards)

    date_yesterday = datetime.utcnow() - timedelta(days=1)

    reports = await HubStaff(user.hub_staff.auth_token).collect_user_activities_by_period(date_yesterday, date_yesterday)

    response = prepare_response_activities_list(reports)
    await message.answer(f"{response}", parse_mode=ParseMode.HTML, reply_markup=activities_keyboards.keyboards)


@dp.message_handler(Text(equals=[WorkLogKeyboards.work_log_week.value]), state=None)
async def get_activity_week(message: types.Message):
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(f"Пользователь не найден.", reply_markup=menu_keyboards.keyboards)

    start_date = datetime.utcnow() - timedelta(days=7)
    end_date = datetime.utcnow()

    reports = await HubStaff(user.hub_staff.auth_token).collect_user_activities_by_period(start_date, end_date)

    response = prepare_response_activities_list(reports)
    await message.answer(f"{response}", parse_mode=ParseMode.HTML, reply_markup=activities_keyboards.keyboards)


