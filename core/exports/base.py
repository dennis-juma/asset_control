from abc import ABC
from abc import abstractmethod


class BaseExporter(ABC):

    @abstractmethod
    def export(
        self,
        grid,
        request,
    ):
        pass