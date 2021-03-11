from enum import Enum


class ServicesEnum(Enum):
    """Enum со списком интегрируемых сервисов используемых в боте."""
    click_up = "ClickUp"
    hub_staff = "HubStaff"


class WebhookUrlsEnum(Enum):
    oauth = "login"
    click_up_webhook_notifications = "clickup/notifications"
