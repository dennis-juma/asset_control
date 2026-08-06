from abc import ABC
from abc import abstractmethod

from core.dtos.dashboard import DashboardWidgetDTO


class DashboardWidget(ABC):

    @abstractmethod
    def build(self) -> DashboardWidgetDTO:
        pass