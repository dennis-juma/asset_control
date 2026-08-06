from django.db.models import Count, Q

from assets.models import Asset
from assets.choices import AssetStatus

from dashboard.dto.stat_card import StatCard
from dashboard.enums import StatFormatter


class StatisticsService:
    """
    Service responsible for generating dashboard KPI cards.

    All dashboard statistics should be calculated here to keep
    views thin and templates free of business logic.
    """

    def get_cards(self) -> list[StatCard]:
        """
        Return all dashboard KPI cards.
        """
        stats = self._get_statistics()

        return [
            self._build_total_assets_card(stats),
            self._build_assigned_assets_card(stats),
            self._build_available_assets_card(stats),
            self._build_maintenance_assets_card(stats),
            self._build_utilisation_card(stats),
        ]

    def _get_statistics(self) -> dict[str, int]:
        """
        Retrieve dashboard statistics using a single database query.
        """
        return Asset.objects.aggregate(
            total=Count("id"),
            assigned=Count(
                "id",
                filter=Q(status=AssetStatus.ASSIGNED),
            ),
            available=Count(
                "id",
                filter=Q(status=AssetStatus.IN_STOCK),
            ),
            maintenance=Count(
                "id",
                filter=Q(status=AssetStatus.MAINTENANCE),
            ),
        )

    def _build_total_assets_card(
        self,
        stats: dict[str, int],
    ) -> StatCard:
        return StatCard(
            title="Total Assets",
            value=stats["total"],
            icon="bi-laptop",
            color="primary",
            subtitle="Registered Assets",
        )

    def _build_assigned_assets_card(
        self,
        stats: dict[str, int],
    ) -> StatCard:
        return StatCard(
            title="Assigned",
            value=stats["assigned"],
            icon="bi-person-check",
            color="success",
            subtitle="Currently Assigned",
        )

    def _build_available_assets_card(
        self,
        stats: dict[str, int],
    ) -> StatCard:
        return StatCard(
            title="Available",
            value=stats["available"],
            icon="bi-box",
            color="warning",
            subtitle="Ready to Assign",
        )

    def _build_maintenance_assets_card(
        self,
        stats: dict[str, int],
    ) -> StatCard:
        return StatCard(
            title="Maintenance",
            value=stats["maintenance"],
            icon="bi-tools",
            color="danger",
            subtitle="Under Maintenance",
        )

    def _build_utilisation_card(
        self,
        stats: dict[str, int],
    ) -> StatCard:
        total_assets = stats["total"]
        assigned_assets = stats["assigned"]

        utilisation = (
            round((assigned_assets / total_assets) * 100, 1)
            if total_assets
            else 0
        )

        return StatCard(
            title="Utilisation",
            value=utilisation,
            icon="bi-graph-up-arrow",
            color="info",
            subtitle="Asset Utilisation",
            formatter=StatFormatter.PERCENTAGE,
        )