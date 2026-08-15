from abc import ABC, abstractmethod


class BaseImporter(ABC):

    @abstractmethod
    def read(self, uploaded_file):
        pass