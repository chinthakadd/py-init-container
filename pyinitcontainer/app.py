import logging

from pyinitcontainer.health.kafka_health_indicator import KafkaHealthIndicator
from pyinitcontainer.health.mongo_health_indicator import MongoHealthIndicator

# Defining main function
def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
    logging.info('Health-check init container start-up')

    # connection to mongo
    mongoHealthIndicator = MongoHealthIndicator()
    mongoHealthIndicator.is_healthy()
    kafkaHealthIndicator = KafkaHealthIndicator()
    kafkaHealthIndicator.is_healthy()

if __name__ == "__main__":
    main()
