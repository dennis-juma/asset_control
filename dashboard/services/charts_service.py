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
    queryset = Asset.objects.all()

    def __init__(self, country=None):
        self.country = country

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
        queryset = Asset.objects.all()

        if self.country:
            queryset = queryset.filter(
                country=self.country,
            )

        status_counts = (
            queryset
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

        queryset = Asset.objects.all()

        if self.country:
            queryset = queryset.filter(
                country=self.country,
            )

        category_counts = (
            queryset
            .values("asset_model__category__name")
            .annotate(total=Count("pk"))
            .order_by("-total")
        )
        labels = []
        values = []

        for item in category_counts:
            labels.append(item["asset_model__category__name"])
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