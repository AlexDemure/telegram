import os

from src.db.settings import MongoDBSettings
from src.submodules.clickup.settings import ClickUpSettings
from src.submodules.hubstaff.settings import HubStaffSettings

# INCLUDE SETTINGS
configs = [MongoDBSettings, ClickUpSettings, HubStaffSettings]


class Settings(*configs):
    TELEGRAM_API_TOKEN: str = os.environ['TELEGRAM_API_TOKEN']

    DAILY_TIME_TRACKED_NORMAL_TO_SECONDS: int = 6 * 60 * 60  # 6h
    DAILY_AVG_ACTIVITY_NORMAL_TO_PERCENTAGE: int = 50

    WEBHOOK_HOST: str = os.environ['WEBHOOK_HOST']
    WEBHOOK_PATH: str = "/webhook"

    WEBHOOK_SSL_CERT = './webhook_cert.pem'
    WEBHOOK_SSL_PRIVATE_KEY = './webhook_pkey.pem'

    @property
    def webhook_uri(self) -> str:
        return f"{self.WEBHOOK_HOST}{self.WEBHOOK_PATH}"


settings = Settings()



