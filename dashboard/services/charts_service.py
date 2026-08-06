from django.db.models import Count

from assets.models import Asset

from dashboard.dto.chart_data import ChartData
from dashboard.dto.chart_dataset import ChartDataset
from dashboard.dto.chart_options import ChartOptions
from dashboard.enums import ChartType


class ChartsService:
    """
    Service responsible for preparing dashboard distribution charts.

    This service only provides charts representing the current state
    of the system. Time-series analytics are handled by TrendService.
    """

    def get_charts(self) -> list[ChartData]:
        """
        Return all dashboard distribution charts.
        """
        return [
            self._asset_status_chart(),
            self._asset_category_chart(),
        ]

    def _asset_status_chart(self) -> ChartData:
        """
        Build asset status distribution chart.
        """

        status_counts = (
            Asset.objects
            .values("status")
            .annotate(total=Count("pk"))
            .order_by("status")
        )

        labels = []
        values = []

        for item in status_counts:
            labels.append(item["status"])
            values.append(item["total"])

        return ChartData(
            chart_id="asset-status-chart",
            title="Asset Status Distribution",
            chart_type=ChartType.DOUGHNUT,
            labels=labels,
            datasets=[
                ChartDataset(
                    label="Assets",
                    data=values,
                ),
            ],
            options=ChartOptions(),
        )

    def _asset_category_chart(self) -> ChartData:
        """
        Build asset category distribution chart.
        """

        category_counts = (
            Asset.objects
            .values("category__name")
            .annotate(total=Count("pk"))
            .order_by("-total")
        )

        labels = []
        values = []

        for item in category_counts:
            labels.append(item["category__name"])
            values.append(item["total"])

        return ChartData(
            chart_id="asset-category-chart",
            title="Assets by Category",
            chart_type=ChartType.BAR,
            labels=labels,
            datasets=[
                ChartDataset(
                    label="Assets",
                    data=values,
                ),
            ],
            options=ChartOptions(),
        )