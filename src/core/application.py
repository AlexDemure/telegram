from aiohttp import web

from src.bot.commands.dispatcher import dp, bot
from src.core import scheduler
from src.core.config import settings
from src.core.urls import routes
from src.db.database import users_db


async def on_startup(app):
    webhook = await bot.get_webhook_info()
    print(webhook)
    users_db.init_connection()
    scheduler.start()

    await bot.set_webhook(f"{settings.webhook_uri}")


async def on_shutdown(app):
    await bot.delete_webhook()


def application():

    app = web.Application()
    app.add_routes(routes)

    app['BOT_DISPATCHER'] = dp

    app.on_startup.append(on_startup)

    return app


if __name__ == '__main__':
    web.run_app(application(), host="127.0.0.1", port=7040)
    #TODO Для продакшена запускать через гуникорн