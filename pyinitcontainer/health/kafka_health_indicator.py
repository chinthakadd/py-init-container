import logging

from kafka import KafkaProducer, KafkaAdminClient
from kafka.errors import NoBrokersAvailable
from retry import retry

from pyinitcontainer.conf.config import settings
from pyinitcontainer.health.health_indicator import HealthIndicator


class KafkaHealthIndicator(HealthIndicator):
    """Implements the HealthIndicator for Kafka by trying to establish a producer connection"""

    __bootstrap_server_url: str
    __kafka_topics: list
    __connection_params: dict
    __logger: logging

    def __init__(self):
        super().__init__()
        self.__bootstrap_server_url = settings.kafka_bootstrap_url
        self.__kafka_topics = [] if 'kafka_topic_list' not in settings else settings.kafka_topic_list
        self.__logger = logging.getLogger(__class__.__name__)

    def is_enabled(self) -> bool:
        return settings.kafka_enabled

    @retry(delay=0.1, tries=settings.kafka_retry_count)
    def is_healthy(self) -> bool:
        try:
            producer = KafkaProducer(bootstrap_servers=self.__bootstrap_server_url)
            producer.close(timeout=1)
            self.__logger.info(msg="Kafka connection successful")
            self.verify_topics()
        except NoBrokersAvailable as nbe:
            self.__logger.error("Kafka connection failed: No brokers available.")
            raise nbe
        except Exception as e:
            self.__logger.error("Exception: %s", e.__class__.__name__, exc_info=True)
            raise e

    def verify_topics(self):
        try:
            self.__logger.info("Checking for Topics: %s", self.__kafka_topics.__str__())
            admin_client = KafkaAdminClient(bootstrap_servers=self.__bootstrap_server_url)
            topics = admin_client.list_topics()
            self.__logger.info("Kafka Broker Topics: %s", str(topics))
            topics_not_created = [t for t in self.__kafka_topics if t not in topics]
            if len(topics_not_created) != 0:
                raise Exception("ERROR: missing " + str(topics_not_created))
        except Exception as e:
            self.__logger.error("Unable to verify topics: %s due to exception",
                                self.__kafka_topics,
                                e.__class__.__name__, exc_info=True)
            raise e
