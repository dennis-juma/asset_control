from core.dashboard.builder import DashboardBuilder
from core.dashboard.widgets.stat import StatWidget


class AssetDashboardProvider:

    def __init__(
        self,
        cards,
        activity,
        chart,
    ):

        self.cards = cards
        self.activity = activity
        self.chart = chart

    def build(self):

        return (
            DashboardBuilder("Asset Dashboard")

            .add_widget(
                StatWidget(
                    "stats",
                    "Asset Statistics",
                    self.cards,
                ).build()
            )

            # Additional widgets added here

            .build()
        )