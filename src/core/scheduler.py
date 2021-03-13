from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.apps.clickup.tasks import daily_send_list_tasks, daily_send_list_tasks_with_unset_time
from src.apps.hubstaff.tasks import daily_send_today_time_tracked_and_activity


def start():
    """Запуск событий по Cron времени."""
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(daily_send_list_tasks, 'cron', hour=9)
    scheduler.add_job(daily_send_list_tasks_with_unset_time, 'cron', hour=9)
    scheduler.add_job(daily_send_today_time_tracked_and_activity, 'cron', hour=20, minute=35)
    scheduler.start()
