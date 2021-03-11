from aiogram.dispatcher.webhook import WebhookRequestHandler
from aiohttp import web

from src.apps.users.routes import login_success_to_system
from src.apps.clickup.routes import accept_notification

from src.core.config import settings
from src.core.enums import WebhookUrlsEnum
from src.utils import get_webhook_url

routes = [
    web.route('get', f"{get_webhook_url(WebhookUrlsEnum.oauth.value)}", login_success_to_system),
    web.route('post', f"{get_webhook_url(WebhookUrlsEnum.click_up_webhook_notifications.value)}", accept_notification),
    web.route('*', settings.WEBHOOK_PATH, WebhookRequestHandler),
]
