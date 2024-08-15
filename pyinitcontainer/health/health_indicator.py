import abc


class HealthIndicator(metaclass=abc.ABCMeta):
    """Base Definition for implementation that checks whether a component is healthy"""

    @abc.abstractmethod
    def is_enabled(self) -> bool:
        """Specifies whether the given health check is run"""
        raise NotImplementedError()

    @abc.abstractmethod
    def is_healthy(self) -> bool:
        """Specifies whether the given resource is healthy"""
        raise NotImplementedError()
