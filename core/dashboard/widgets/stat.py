from core.dashboard.base import DashboardWidget
from core.dashboard.enums import WidgetType
from core.dtos.dashboard import DashboardWidgetDTO


class StatWidget(DashboardWidget):

    def __init__(
        self,
        widget_id,
        title,
        cards,
    ):

        self.widget_id = widget_id
        self.title = title
        self.cards = cards

    def build(self):

        return DashboardWidgetDTO(
            id=self.widget_id,
            title=self.title,
            widget_type=WidgetType.STAT,
            template="dashboard/stat.html",
            data=self.cards,
            width=12,
        )