from aiogram.dispatcher.webhook import WebhookRequestHandler
from aiohttp import web

from src.apps.users.routes import login_success_to_system
from src.core.config import settings
from src.submodules.oauth.settings import OAUTH_ENDPOINT
from src.utils import get_webhook_url

routes = [
    web.route('get', f"{get_webhook_url(OAUTH_ENDPOINT)}", login_success_to_system),
    web.route('*', settings.WEBHOOK_PATH, WebhookRequestHandler),
]
