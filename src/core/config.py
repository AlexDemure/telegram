import os

from src.db.settings import MongoDBSettings
from src.submodules.clickup.settings import ClickUpSettings
from src.submodules.hubstaff.settings import HubStaffSettings

# INCLUDE SETTINGS
configs = [MongoDBSettings, ClickUpSettings, HubStaffSettings]


class Settings(*configs):
    TELEGRAM_API_TOKEN: str = os.environ['TELEGRAM_API_TOKEN']


settings = Settings()



