import os

from src.db.settings import MongoDBSettings

# INCLUDE SETTINGS
configs = [MongoDBSettings]


class Settings(*configs):
    TELEGRAM_API_TOKEN: str = os.environ['TELEGRAM_API_TOKEN']
    CLICKUP_CLIENT_ID: str = os.environ['CLICKUP_CLIENT_ID']
    CLICKUP_SECRET_KEY: str = os.environ['CLICKUP_SECRET_KEY']


settings = Settings()


