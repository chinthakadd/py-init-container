import logging

from pyinitcontainer.health.health_indicator import HealthIndicator


class InfrastructureHealthIndicator(HealthIndicator):
    """Represents all HealthIndicators that are part of the infrastructure"""

    __component_health_indicators: list[HealthIndicator]
    __logger: logging

    def __init__(self, health_indicators: list[HealthIndicator]):
        super().__init__()
        self.__component_health_indicators = health_indicators
        self.__logger = logging.getLogger(self.__class__.__name__)

    def is_enabled(self) -> bool:
        return True

    def is_healthy(self) -> bool:
        """Runs all HealthIndicator implementations which are enabled"""
        for hi in self.__component_health_indicators:
            if hi.is_enabled():
                self.__logger.info("Initiating Health Check for %s", hi.__class__.__name__)
                hi.is_healthy()
                self.__logger.info("%s - Completed", hi.__class__.__name__)
            else:
                self.__logger.warning("%s - Not Active", hi.__class__.__name__)
