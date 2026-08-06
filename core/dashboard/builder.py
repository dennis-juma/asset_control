from core.dtos.dashboard import (
    DashboardDTO,
    DashboardWidgetDTO,
)


class DashboardBuilder:

    def __init__(self, title):

        self.dashboard = DashboardDTO(
            title=title,
        )

    def add_widget(
        self,
        widget: DashboardWidgetDTO,
    ):

        self.dashboard.widgets.append(widget)

        return self

    def build(self):

        return self.dashboard
    

    