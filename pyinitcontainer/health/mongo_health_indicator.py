from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from pyinitcontainer.conf.config import settings
from pyinitcontainer.health.health_indicator import HealthIndicator


class MongoHealthIndicator(HealthIndicator):
    """This health indicator checks health of mongo"""

    __mongo_url: str

    def __init__(self):
        super().__init__()
        self.__mongo_url = settings.mongo_url

    def is_healthy(self) -> bool:
        try:
            # Create a MongoClient to the running MongoDB instance
            client = MongoClient(self.__mongo_url)
            # The ismaster command is cheap and does not require authentication
            client.admin.command('ismaster')
            print("MongoDB connection successful.")
            return True
        except ConnectionFailure as e:
            print(f"MongoDB connection failed: {e}")
            return False
