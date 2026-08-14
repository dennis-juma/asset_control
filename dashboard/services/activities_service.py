
from datetime import date, datetime, time

from django.utils import timezone

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
    def __init__(self, country=None):
        self.country = country
    # =====================================================
    # Helpers
    # =====================================================

    @staticmethod
    def _as_datetime(value):
        """
        Normalize activity timestamps to timezone-aware datetimes.

        Handles:
        - datetime
        - date
        - None
        """

        if value is None:
            return None

        if isinstance(value, datetime):

            if timezone.is_naive(value):
                return timezone.make_aware(
                    value,
                    timezone.get_current_timezone(),
                )

            return value

        if isinstance(value, date):

            value = datetime.combine(
                value,
                time.min,
            )

            return timezone.make_aware(
                value,
                timezone.get_current_timezone(),
            )

        return value

    # =====================================================
    # Recent Activities
    # =====================================================

    def get_recent_activities(self) -> list[ActivityDTO]:

        activities: list[ActivityDTO] = []

        activities.extend(
            self._get_asset_activities()
        )

        activities.extend(
            self._get_assignment_activities()
        )

        activities.extend(
            self._get_return_activities()
        )

        activities.extend(
            self._get_maintenance_activities()
        )

        activities.sort(
            key=lambda activity: activity.timestamp,
            reverse=True,
        )

        return activities[: self.DASHBOARD_LIMIT]

    # =====================================================
    # Asset Activities
    # =====================================================

    def _get_asset_activities(
        self,
    ) -> list[ActivityDTO]:
        queryset = Asset.objects.select_related(
        "asset_model",
    )
        
        if self.country:
            queryset = queryset.filter(
                country=self.country,
            )

        assets = queryset.order_by(
            "-created_at"
        )[: self.ACTIVITY_LIMIT]

        return [
            ActivityDTO(
                title="Asset Registered",

                description=(
                    f"{asset.asset_tag} "
                    f"was registered."
                ),

                icon="bi bi-laptop",

                color="primary",

                timestamp=self._as_datetime(
                    asset.created_at,
                ),

                url=None,
            )
            for asset in assets
        ]

    # =====================================================
    # Assignment Activities
    # =====================================================

    def _get_assignment_activities(
        self,
    ) -> list[ActivityDTO]:

        queryset = AssetAssignment.objects.select_related(
    "asset",
    "employee",
    "site",
).filter(
    status="ACTIVE",
)

        if self.country:
            queryset = queryset.filter(
                country=self.country,
            )

        assignments = queryset.order_by(
            "-assigned_date"
        )[: self.ACTIVITY_LIMIT]

        return [
            ActivityDTO(
                title="Asset Assigned",

                description=(
                    f"{assignment.asset.asset_tag} "
                    f"assigned to "
                    f"{assignment.assigned_to_name}."
                ),

                icon="bi bi-person-check",

                color="success",

                timestamp=self._as_datetime(
                    assignment.assigned_date,
                ),

                url=None,
            )
            for assignment in assignments
        ]

    # =====================================================
    # Return Activities
    # =====================================================

    def _get_return_activities(
        self,
    ) -> list[ActivityDTO]:

        queryset = AssetAssignment.objects.select_related(
    "asset",
    "employee",
    "site",
).filter(
    returned_date__isnull=False,
)

        if self.country:
            queryset = queryset.filter(
                country=self.country,
            )

        returns = queryset.order_by(
            "-returned_date"
        )[: self.ACTIVITY_LIMIT]

        return [
            ActivityDTO(
                title="Asset Returned",

                description=(
                    f"{assignment.asset.asset_tag} "
                    f"returned from "
                    f"{assignment.assigned_to_name}."
                ),

                icon="bi bi-arrow-return-left",

                color="warning",

                timestamp=self._as_datetime(
                    assignment.returned_date,
                ),

                url=None,
            )
            for assignment in returns
            if assignment.returned_date
        ]

    # =====================================================
    # Maintenance Activities
    # =====================================================

    def _get_maintenance_activities(
        self,
    ) -> list[ActivityDTO]:

        queryset = Maintenance.objects.select_related(
    "asset",
)

        if self.country:
            queryset = queryset.filter(
                country=self.country,
            )

        maintenances = queryset.order_by(
            "-created_at"
        )[: self.ACTIVITY_LIMIT]

        return [
            ActivityDTO(
                title="Maintenance Scheduled",

                description=(
                    f"{maintenance.asset.asset_tag} "
                    f"scheduled for maintenance."
                ),

                icon="bi bi-tools",

                color="info",

                timestamp=self._as_datetime(
                    maintenance.created_at,
                ),

                url=None,
            )
            for maintenance in maintenances
        ]