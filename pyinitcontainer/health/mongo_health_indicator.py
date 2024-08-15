import logging

from pymongo import MongoClient
from retry import retry

from pyinitcontainer.conf.config import settings
from pyinitcontainer.health.health_indicator import HealthIndicator


class MongoHealthIndicator(HealthIndicator):
    """ This health indicator checks health of mongo that tries to execute an admin command against the master"""

    # Mongo Connection URL.
    __mongo_url: str
    __logger: logging

    def __init__(self):
        super().__init__()
        self.__mongo_url = settings.mongo_url
        self.__logger = logging.getLogger(__class__.__name__)

    def is_enabled(self) -> bool:
        return settings.mongo_enabled

    @retry(delay=0.1, tries=settings.mongo_retry_count)
    def is_healthy(self) -> bool:
        """Runs the health check and retries until fails. Retry count is configurable"""
        try:
            # Create a MongoClient to the running MongoDB instance
            client = MongoClient(self.__mongo_url, timeoutMS=100)
            # The ismaster command is cheap and does not require authentication
            self.__logger.info(client.admin.command('ismaster'))
            self.__logger.info("MongoDB connection successful.")
            return True
        except Exception as e:
            self.__logger.error("Kafka connection failed: %s", e.__class__.__name__, exc_info=True)
            raise e
