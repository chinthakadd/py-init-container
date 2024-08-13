from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

from pyinitcontainer.conf.config import settings
from pyinitcontainer.health.health_indicator import HealthIndicator


class KafkaHealthIndicator(HealthIndicator):
    """Implements the HealthIndicator for Kafka"""

    __bootstrap_server_url: str
    __connection_params: dict

    def __init__(self):
        super().__init__()
        self.__bootstrap_server_url = settings.kafka_bootstrap_url

    def is_healthy(self) -> bool:
        try:
            producer = KafkaProducer(bootstrap_servers = self.__bootstrap_server_url)
            producer.close(timeout=10)
            print("Kafka connection successful")
            return True
        except NoBrokersAvailable:
            print("Kafka connection failed: No brokers available.")
        except Exception as e:
            print(f"Kafka connection failed: {e}")
        return False
