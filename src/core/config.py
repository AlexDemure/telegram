import os

from src.db.settings import MongoDBSettings
from src.submodules.clickup.settings import ClickUpSettings
from src.submodules.hubstaff.settings import HubStaffSettings

# INCLUDE SETTINGS
configs = [MongoDBSettings, ClickUpSettings, HubStaffSettings]


class Settings(*configs):
    TELEGRAM_API_TOKEN: str = os.environ['TELEGRAM_API_TOKEN']

    DAILY_TIME_TRACKED_NORMAL_TO_SECONDS = 6 * 60 * 60  # 6h
    DAILY_AVG_ACTIVITY_NORMAL_TO_PERCENTAGE = 50


settings = Settings()



