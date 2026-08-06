from abc import ABC
from abc import abstractmethod

from core.dtos.badge import BadgeDTO


class BadgeProvider(ABC):

    @abstractmethod
    def build(self, value) -> BadgeDTO:
        pass