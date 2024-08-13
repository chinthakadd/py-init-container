import abc


class HealthIndicator(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def is_healthy(self) -> bool:
        """Specifies whether the given resource is healthy"""
        raise NotImplementedError()
