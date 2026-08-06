from assets.models import Asset
from assets.models.asset_assignment import AssetAssignment
from maintenance.models import Maintenance

from dashboard.dto.activity import ActivityDTO


class ActivityService:
    """
    Aggregates recent dashboard activities from multiple modules.
    """

    ACTIVITY_LIMIT = 5
    DASHBOARD_LIMIT = 10

    def get_recent_activities(self) -> list[ActivityDTO]:
        activities: list[ActivityDTO] = []

        activities.extend(self._get_asset_activities())
        activities.extend(self._get_assignment_activities())
        activities.extend(self._get_return_activities())
        activities.extend(self._get_maintenance_activities())

        activities.sort(
            key=lambda activity: activity.timestamp,
            reverse=True,
        )

        return activities[: self.DASHBOARD_LIMIT]

    def _get_asset_activities(self) -> list[ActivityDTO]:
        assets = (
            Asset.objects.select_related("model")
            .order_by("-created_at")[: self.ACTIVITY_LIMIT]
        )

        return [
            ActivityDTO(
                title="Asset Registered",
                description=f"{asset.asset_tag} was registered.",
                icon="bi bi-laptop",
                color="primary",
                timestamp=asset.created_at,
                url=None,
            )
            for asset in assets
        ]

    def _get_assignment_activities(self) -> list[ActivityDTO]:
        assignments = (
            AssetAssignment.objects.select_related(
                "asset",
                "employee",
            )
            .order_by("-assigned_date")[: self.ACTIVITY_LIMIT]
        )

        return [
            ActivityDTO(
                title="Asset Assigned",
                description=(
                    f"{assignment.asset.asset_tag} assigned to "
                    f"{assignment.employee}"
                ),
                icon="bi bi-person-check",
                color="success",
                timestamp=assignment.assigned_date,
                url=None,
            )
            for assignment in assignments
        ]

    def _get_return_activities(self) -> list[ActivityDTO]:
        returns = (
            AssetAssignment.objects.select_related(
                "asset",
                "employee",
            )
            .filter(returned_date__isnull=False)
            .order_by("-returned_date")[: self.ACTIVITY_LIMIT]
        )

        return [
            ActivityDTO(
                title="Asset Returned",
                description=(
                    f"{assignment.asset.asset_tag} returned by "
                    f"{assignment.employee}"
                ),
                icon="bi bi-arrow-return-left",
                color="warning",
                timestamp=assignment.returned_date,
                url=None,
            )
            for assignment in returns
            if assignment.returned_date
        ]

    def _get_maintenance_activities(self) -> list[ActivityDTO]:
        maintenances = (
            Maintenance.objects.select_related("asset")
            .order_by("-created_at")[: self.ACTIVITY_LIMIT]
        )

        return [
            ActivityDTO(
                title="Maintenance Scheduled",
                description=(
                    f"{maintenance.asset.asset_tag} "
                    f"scheduled for maintenance."
                ),
                icon="bi bi-tools",
                color="info",
                timestamp=maintenance.created_at,
                url=None,
            )
            for maintenance in maintenances
        ]