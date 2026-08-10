from datetime import timedelta

from django.utils import timezone

from assets.models import Asset
from assets.models.asset_assignment import AssetAssignment
from maintenance.models import Maintenance

from assets.choices.choices import AssignmentStatus
from maintenance.choices import MaintenanceStatus

from dashboard.dto.alert import AlertDTO


class AlertService:
    """
    Builds operational alerts displayed on the dashboard.
    """

    def get_alerts(self) -> list[AlertDTO]:
        alerts: list[AlertDTO] = []

        alert = self._maintenance_alert()
        if alert:
            alerts.append(alert)

        alert = self._overdue_return_alert()
        if alert:
            alerts.append(alert)

        alert = self._overdue_maintenance_alert()
        if alert:
            alerts.append(alert)

    

        return alerts

    def _maintenance_alert(self) -> AlertDTO | None:
        count = Maintenance.objects.filter(
            status=MaintenanceStatus.IN_PROGRESS,
        ).count()

        if not count:
            return None

        return AlertDTO(
            title="Assets Under Maintenance",
            description="Assets currently undergoing maintenance.",
            icon="bi bi-tools",
            color="warning",
            count=count,
        )

    def _overdue_return_alert(self) -> AlertDTO | None:
        today = timezone.now().date()

        count = (
            AssetAssignment.objects.filter(
                status=AssignmentStatus.ACTIVE,
                expected_return_date__lt=today,
            ).count()
        )

        if not count:
            return None

        return AlertDTO(
            title="Overdue Returns",
            description="Assets that should have been returned.",
            icon="bi bi-arrow-return-left",
            color="danger",
            count=count,
        )

    def _overdue_maintenance_alert(self) -> AlertDTO | None:
        today = timezone.now().date()

        count = (
            Maintenance.objects.filter(
                status=MaintenanceStatus.SCHEDULED,
                scheduled_date__lt=today,
            ).count()
        )

        if not count:
            return None

        return AlertDTO(
            title="Overdue Maintenance",
            description="Scheduled maintenance awaiting execution.",
            icon="bi bi-exclamation-triangle",
            color="danger",
            count=count,
        )

    