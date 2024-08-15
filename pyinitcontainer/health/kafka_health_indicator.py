import logging

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from retry import retry

from pyinitcontainer.conf.config import settings
from pyinitcontainer.health.health_indicator import HealthIndicator


class KafkaHealthIndicator(HealthIndicator):
    """Implements the HealthIndicator for Kafka by trying to establish a producer connection"""

    __bootstrap_server_url: str
    __connection_params: dict
    __logger: logging

    def __init__(self):
        super().__init__()
        self.__bootstrap_server_url = settings.kafka_bootstrap_url
        self.__logger = logging.getLogger(__class__.__name__)

    def is_enabled(self) -> bool:
        return settings.kafka_enabled

    @retry(delay=0.1, tries=settings.kafka_retry_count)
    def is_healthy(self) -> bool:
        try:
            producer = KafkaProducer(bootstrap_servers=self.__bootstrap_server_url)
            producer.close(timeout=1)
            self.__logger.info(msg="Kafka connection successful")
            return True
        except NoBrokersAvailable as nbe:
            self.__logger.error("Kafka connection failed: No brokers available.")
            raise nbe
        except Exception as e:
            self.__logger.error("Kafka connection failed: %s", e.__class__.__name__, exc_info=True)
            raise e
