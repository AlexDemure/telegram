import logging

from aiohttp import web

from src.bot.dispatcher import dp, bot
from src.core import scheduler
from src.core.config import settings
from src.core.urls import routes
from src.db.database import users_db

from src.submodules.clickup.service import ClickUp
from src.utils import get_webhook_url
from src.core.enums import WebhookUrlsEnum


async def on_startup(app):
    webhook = await bot.get_webhook_info()
    logging.info(f"Webhook data: {webhook}")

    users_db.init_connection()
    scheduler.start()

    await bot.delete_webhook()
    await bot.set_webhook(f"{settings.webhook_uri}")

    # Отправка уведомлений в ClickUP что по этой команде мы ждем уведомления.
    # TODO Выбор спейсов
    # TODO ДОбавить удаление ClickUp
    await ClickUp("6655746_f2d0df7798fd0e1952c7a4123ba2fc00eaf354c3").start_webhook_accepting(
        team_id=2604924,
        webhook_endpoint=get_webhook_url(
            WebhookUrlsEnum.click_up_webhook_notifications.value,
            short_url=False
        )
    )

async def on_shutdown(app):
    dispatcher = app['BOT_DISPATCHER']
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

    await bot.delete_webhook()


def application():

    app = web.Application()
    app.add_routes(routes)

    app['BOT_DISPATCHER'] = dp

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    return app


if __name__ == '__main__':
    web.run_app(application(), host="127.0.0.1", port=7040)
    #TODO Для продакшена запускать через гуникорн