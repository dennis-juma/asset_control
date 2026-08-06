from abc import ABC, abstractmethod

from core.dtos import GridCell


class CellRenderer(ABC):
    """
    Base class for all cell renderers.
    """

    @abstractmethod
    def render(self, value) -> GridCell:
        raise NotImplementedError