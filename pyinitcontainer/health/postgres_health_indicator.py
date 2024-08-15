import logging

import psycopg2
from retry import retry

from pyinitcontainer.conf.config import settings
from pyinitcontainer.health.health_indicator import HealthIndicator


class PostgresHealthIndicator(HealthIndicator):
    """ This health indicator checks health of postgres db with a select statement that requires DB credentials"""

    # Postgres Connection URL.
    __postgres_host: str
    __postgres_port: str
    __postgres_user: str
    __postgres_pwd: str
    __postgres_db: str

    __logger: logging

    def __init__(self):

        super().__init__()
        self.__postgres_host = settings.postgres_host
        self.__postgres_port = settings.postgres_port
        self.__postgres_user = settings.postgres_user
        self.__postgres_pwd = settings.postgres_pwd
        self.__postgres_db = settings.postgres_db

        self.__logger = logging.getLogger(__class__.__name__)

    def is_enabled(self) -> bool:
        return settings.postgres_enabled

    @retry(delay=0.1, tries=settings.postgres_retry_count)
    def is_healthy(self) -> bool:
        try:
            # Update with your actual PostgreSQL connection details
            connection = psycopg2.connect(
                user=self.__postgres_user,
                password=self.__postgres_pwd,
                host=self.__postgres_host,
                port=self.__postgres_port,
                database=self.__postgres_db
            )
            cursor = connection.cursor()
            cursor.execute("SELECT 1;")
            cursor.close()
            connection.close()
            self.__logger.info("Postgres connection successful.")
            return True
        except Exception as e:
            self.__logger.error("Postgres connection failed: %s", e.__class__.__name__, exc_info=True)
            raise e
