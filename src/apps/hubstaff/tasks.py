import logging
from datetime import datetime

from aiogram.types import ParseMode

from src.apps.hubstaff.logic import get_activities_by_period
from src.apps.users.logic import get_users
from src.bot.dispatcher import bot
from src.bot.messages.hubstaff.activities import (
    prepare_response_today_time_tracked, prepare_response_today_activity
)


async def daily_send_today_time_tracked_and_activity():
    """Ежедневная отправка уведомлений о проставленном времени за сегодня."""
    start_date = end_date = datetime.utcnow()

    users = await get_users()
    for user in users:
        if getattr(user, 'hub_staff', None) is None:
            logging.info(f'User have not connection to HubStaff {user.dict()}')
            continue

        reports = await get_activities_by_period(user, start_date, end_date)
        time_tracked_response = prepare_response_today_time_tracked(reports)
        activity_tracked_response = prepare_response_today_activity(reports)
        await bot.send_message(user.user_id, time_tracked_response, parse_mode=ParseMode.HTML)
        await bot.send_message(user.user_id, activity_tracked_response, parse_mode=ParseMode.HTML)

