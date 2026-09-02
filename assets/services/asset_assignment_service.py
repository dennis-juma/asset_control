from django.db import transaction
from assets.choices.history_choices import AssetHistoryEvent
from assets.services.asset_history_service import AssetHistoryService
from assets.services.asset_service import AssetService


from assets.choices import (
    AssetStatus,
    AssignmentStatus,
    AssignmentType
)
from assets.dtos import (
    AssetAssignmentCreateDTO,
    AssetAssignmentUpdateDTO,
    AssetReturnDTO,
)
from assets.models import AssetAssignment
from assets.repositories import (
    AssetAssignmentRepository,
)
from assets.validators import (
    AssetAssignmentValidator,
)
from django.utils import timezone
from core.notifications.service import NotificationService
from core.notifications.enums import NotificationEvent
from assets.services.asset_notification_service import AssetNotificationService


class AssetAssignmentService:

    def __init__(self):
        self.repository = AssetAssignmentRepository()
        self.validator = AssetAssignmentValidator()

    # =====================================================
    # Assign Asset
    # =====================================================

    @transaction.atomic
    def create(
        self,
        dto: AssetAssignmentCreateDTO,
    ) -> AssetAssignment:

        self.validator.validate_create(dto)

        assignment = AssetAssignment(
            country=dto.country,
            asset=dto.asset,
            assignment_type=dto.assignment_type,
            employee=dto.employee,
            site=(
                dto.employee.site
                if dto.employee
                else dto.site
            ),
            assigned_date=dto.assigned_date,
            expected_return_date=dto.expected_return_date,
            remarks=dto.remarks,
            status=AssignmentStatus.ACTIVE,
        )

        assignment = self.repository.create(
            assignment
        )

        asset = dto.asset

        old_status = asset.status

        asset.status = AssetStatus.ASSIGNED

        asset.save(
            update_fields=["status"]
        )

        AssetHistoryService.log_event(
    asset=asset,
    event_type=AssetHistoryEvent.ASSIGNED,
    employee=assignment.employee,
    site=assignment.site,
    old_status=old_status,
    new_status=AssetStatus.ASSIGNED,
    reference=str(assignment.pk),
    notes=dto.remarks or "Asset assigned.",
)

        # Send email notification when assignment is effective today
        try:
            if (
                dto.assigned_date == timezone.localdate()
                and assignment.employee
                and getattr(assignment.employee, "user", None)
                and getattr(assignment.employee.user, "email", "")
            ):
                assigned_assets = AssetNotificationService.employee_assets(
                    assignment.employee
                )

                NotificationService.send_email(
                    event=NotificationEvent.ASSET_ASSIGNED,
                    recipient=assignment.employee.user,
                    subject="New Asset Assigned",
                    template="emails/asset_assigned.html",
                    context={
                        "employee": assignment.employee,
                        "assignment": assignment,
                        "assigned_assets": assigned_assets,
                        "asset_count": assigned_assets.count(),
                    },
                )
        except Exception:
            # Email failures should not block assignment creation.
            pass

        return assignment

    # =====================================================
    # Update Assignment
    # =====================================================

    @transaction.atomic
    def update(
        self,
        assignment: AssetAssignment,
        dto: AssetAssignmentUpdateDTO,
    ) -> AssetAssignment:

        self.validator.validate_update(
            assignment,
            dto,
        )
        assignment.assignment_type =dto.assignment_type

        assignment.employee = dto.employee
        assignment.site = dto.employee.site if dto.employee else dto.site
        assignment.assigned_date = dto.assigned_date
        assignment.expected_return_date = dto.expected_return_date
        assignment.remarks = dto.remarks
        assignment.is_active = dto.is_active

        return self.repository.update(assignment)

    # =====================================================
    # Return Asset
    # =====================================================

    @transaction.atomic
    def return_asset(
        self,
        assignment: AssetAssignment,
        dto: AssetReturnDTO,
    ) -> AssetAssignment:

        assignment.returned_date = dto.returned_date
        assignment.status = AssignmentStatus.RETURNED
        assignment.remarks = dto.remarks

        assignment = self.repository.update(
            assignment
        )

        asset = assignment.asset

        old_status = asset.status

        asset.status = AssetStatus.AVAILABLE

        asset.save(
            update_fields=["status"]
        )

        AssetHistoryService.log_event(
            asset=asset,
            event_type=AssetHistoryEvent.RETURNED,
            employee=assignment.employee,
            site=assignment.site,
            old_status=old_status,
            new_status=AssetStatus.AVAILABLE,
            reference=str(assignment.pk),
            notes=dto.remarks or "Asset returned.",
        )

        return assignment