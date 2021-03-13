import logging

from aiohttp import web

from src.bot.dispatcher import dp, bot
from src.core import scheduler
from src.core.config import settings
from src.core.urls import routes
from src.db.database import users_db

from src.apps.clickup.logic import webhook_contoller


async def on_startup(app):
    webhook = await bot.get_webhook_info()
    logging.info(f"Webhook data: {webhook}")

    users_db.init_connection()
    scheduler.start()

    await bot.delete_webhook()
    await bot.set_webhook(f"{settings.webhook_uri}")

    logging.debug(f"Webhook start lists: {await webhook_contoller.webhook_list()}")
    await webhook_contoller.init_connection()
    logging.debug(f"Webhook lists after connection: {await webhook_contoller.webhook_list()}")


async def on_shutdown(app):
    dispatcher = app['BOT_DISPATCHER']
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

    await bot.delete_webhook()

    await webhook_contoller.clear_webhooks()


async def application():

    app = web.Application()
    app.add_routes(routes)

    app['BOT_DISPATCHER'] = dp

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    return app

if __name__ == '__main__':
    web.run_app(application(), host="0.0.0.0", port=7040)
