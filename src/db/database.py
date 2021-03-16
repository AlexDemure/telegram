import logging

from motor import motor_asyncio

from src.core.config import settings


class AIOMotor:

    db_name: str = None
    collection_name: str = None
    connect_uri: str = None

    client = None
    db = None
    collection = None

    def __init__(self, db_name: str, collection_name: str, uri: str):
        self.db_name = db_name
        self.collection_name = collection_name
        self.connect_uri = uri

    def init_connection(self):
        logging.info(
            f"Connect to MongoDB: db:{self.db_name}, collection:{self.collection_name}, uri:{self.connect_uri}"
        )
        self.client = motor_asyncio.AsyncIOMotorClient(self.connect_uri)
        self.db = self.client[self.db_name]
        self.collection = self.db.get_collection(self.collection_name)


users_db = AIOMotor("telegram", "users", settings.get_uri())

