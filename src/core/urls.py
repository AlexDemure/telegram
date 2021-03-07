from aiogram.dispatcher.webhook import WebhookRequestHandler
from aiohttp import web

from src.apps.users.routes import login_to_system
from src.core.config import settings


def get_webhook_url(endpoint: str, short_url=True) -> str:
    if short_url:
        return f"{settings.WEBHOOK_PATH}/{endpoint}"
    else:
        return f"{settings.webhook_uri}/{endpoint}"


OAUTH_ENDPOINT = "login"


routes = [
    web.route('get', f"{get_webhook_url(OAUTH_ENDPOINT)}", login_to_system),
    web.route('*', settings.WEBHOOK_PATH, WebhookRequestHandler),
]
