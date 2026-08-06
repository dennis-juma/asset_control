from abc import ABC
from abc import abstractmethod


class BaseSearchProvider(ABC):

    @abstractmethod
    def search(
        self,
        user,
        query,
    ):
        pass