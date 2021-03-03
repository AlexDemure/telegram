from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.commands.clickup.tasks import daily_send_list_tasks, daily_send_list_tasks_with_unset_time


def start():
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(daily_send_list_tasks, 'cron', hour=8)
    scheduler.add_job(daily_send_list_tasks_with_unset_time, 'cron', hour=8, minute=10)
    scheduler.start()
