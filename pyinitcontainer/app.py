import logging

from pyinitcontainer.conf.log_formatter import LogFormatter
from pyinitcontainer.health.infrastructure_health_indicator import InfrastructureHealthIndicator
from pyinitcontainer.health.kafka_health_indicator import KafkaHealthIndicator
from pyinitcontainer.health.kafka_topic_health_indicator import KafkaTopicHealthIndicator
from pyinitcontainer.health.mongo_health_indicator import MongoHealthIndicator
from pyinitcontainer.health.postgres_health_indicator import PostgresHealthIndicator

log_format = "%(name)s | %(levelname)s | %(asctime)s | %(message)s"
# initialize logging
logging.basicConfig(
    datefmt="%Y-%m-%dT%H:%M:%SZ",
    level=logging.INFO
)
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(LogFormatter(log_format))
logging.getLogger().removeHandler(logging.getLogger().handlers[0])
logging.getLogger().addHandler(stdout_handler)


# Defining main function
def main():
    # connection to mongo
    InfrastructureHealthIndicator(
        [
            KafkaHealthIndicator(), MongoHealthIndicator(), KafkaTopicHealthIndicator(), PostgresHealthIndicator()
        ]
    ).is_healthy()


if __name__ == "__main__":
    logging.getLogger().info('Health-check init container start-up')
    main()
