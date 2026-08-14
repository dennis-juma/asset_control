from django.db.models import Count
from django.db.models.functions import TruncMonth

from assets.models import AssetAssignment
from maintenance.models import Maintenance

from dashboard.dto.chart_data import ChartData
from dashboard.dto.chart_dataset import ChartDataset
from dashboard.enums import ChartType


class TrendService:
    """
    Builds all dashboard trend analytics.
    """
    def __init__(self, country=None):
        self.country = country

    def get_trends(self) -> list[ChartData]:
        return [
            self._assignment_trend(),
            self._maintenance_trend(),
        ]

    def _group_by_period(
        self,
        queryset,
        date_field: str,
    ) -> tuple[list[str], list[int]]:
        """
        Aggregate records by month.
        """

        results = (
            queryset
            .annotate(period=TruncMonth(date_field))
            .values("period")
            .annotate(total=Count("pk"))
            .order_by("period")
        )

        labels = []
        values = []

        for row in results:
            labels.append(row["period"].strftime("%b %Y"))
            values.append(row["total"])

        return labels, values

    def _assignment_trend(self) -> ChartData:
        queryset = AssetAssignment.objects.all()

        if self.country:
            queryset = queryset.filter(
                country=self.country,
            )

        labels, values = self._group_by_period(
            queryset,
            "assigned_date",
        )

        return ChartData(
            chart_id="assignment-trend",
            title="Asset Assignment Trend",
            chart_type=ChartType.LINE,
            labels=labels,
            datasets=[
                ChartDataset(
                    label="Assignments",
                    data=values,
                )
            ],
        )

    def _maintenance_trend(self) -> ChartData:
        labels, values = self._group_by_period(
            Maintenance.objects.all(),
            "scheduled_date",
        )

        return ChartData(
            chart_id="maintenance-trend",
            title="Maintenance Schedule Trend",
            chart_type=ChartType.LINE,
            labels=labels,
            datasets=[
                ChartDataset(
                    label="Maintenance",
                    data=values,
                )
            ],
        )