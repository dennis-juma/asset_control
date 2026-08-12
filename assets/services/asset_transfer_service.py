from django.db import transaction
from django.core.exceptions import ValidationError
from assets.choices.history_choices import AssetHistoryEvent
from assets.services.asset_history_service import AssetHistoryService

from assets.choices import (
    AssignmentStatus,
    AssignmentType,
    AssetStatus,
)

from assets.dtos.asset_transfer import (
    AssetTransferCreateDTO,
    AssetTransferUpdateDTO,
)

from assets.models import AssetAssignment
from assets.models.asset_transfer import AssetTransfer

from assets.repositories import (
    AssetAssignmentRepository,
    AssetTransferRepository,
)

from assets.validators import (
    AssetTransferValidator,
)


class AssetTransferService:

    def __init__(self):
        self.repository = AssetTransferRepository()
        self.assignment_repository = (
            AssetAssignmentRepository()
        )
        self.validator = AssetTransferValidator()

    # =====================================================
    # Create Transfer
    # =====================================================

    @transaction.atomic
    def create(
        self,
        dto: AssetTransferCreateDTO,
    ) -> AssetTransfer:

        # -------------------------------------------------
        # 1. Get current active assignment
        # -------------------------------------------------

        previous_assignment = (
            self.repository.get_active_assignment(
                dto.asset,
            )
        )

        if previous_assignment is None:
            raise ValidationError(
                {
                    "asset":
                    "This asset does not have an active assignment."
                }
            )

        # -------------------------------------------------
        # 2. Make sure DTO uses current assignment
        # -------------------------------------------------

        dto.previous_assignment = previous_assignment

        # -------------------------------------------------
        # 3. Validate transfer
        # -------------------------------------------------

        self.validator.validate_create(
            dto,
        )

        # -------------------------------------------------
        # 4. Capture current source
        # -------------------------------------------------

        from_employee = (
            previous_assignment.employee
        )

        from_site = (
            previous_assignment.site
        )

        # -------------------------------------------------
        # 5. Determine target
        # -------------------------------------------------

        to_employee = dto.to_employee
        to_site = dto.to_site

        if dto.to_employee is not None:
            assignment_type = (
                AssignmentType.EMPLOYEE
            )
        else:
            assignment_type = (
                AssignmentType.SITE
            )

        # -------------------------------------------------
        # 6. Close previous assignment
        # -------------------------------------------------

        previous_assignment.status = (
            AssignmentStatus.TRANSFERRED
        )

        previous_assignment.returned_date = (
            None
        )

        previous_assignment.save(
            update_fields=[
                "status",
                "returned_date",
                "updated_at",
            ]
        )

        # -------------------------------------------------
        # 7. Create new assignment
        # -------------------------------------------------

        new_assignment = AssetAssignment.objects.create(
            company=dto.company,
            asset=dto.asset,
            assignment_type=assignment_type,
            employee=to_employee,
            site=to_site,
            assigned_date=dto.transfer_date,
            expected_return_date=None,
            status=AssignmentStatus.ACTIVE,
            remarks=(
                f"Transferred from "
                f"{previous_assignment.assigned_to_name}."
            ),
        )

        # -------------------------------------------------
        # 8. Create transfer record
        # -------------------------------------------------

        transfer = self.repository.create(
            company=dto.company,
            asset=dto.asset,
            previous_assignment=previous_assignment,
            new_assignment=new_assignment,
            from_employee=from_employee,
            from_site=from_site,
            to_employee=to_employee,
            to_site=to_site,
            transfer_date=dto.transfer_date,
            reason=dto.reason or "",
            remarks=dto.remarks or "",
        )
        AssetHistoryService.log_event(
    asset=dto.asset,
    event_type=AssetHistoryEvent.TRANSFERRED,
    employee=to_employee,
    site=to_site,
    old_status=AssetStatus.ASSIGNED,
    new_status=AssetStatus.ASSIGNED,
    reference=str(transfer.pk),
    notes=dto.reason or "Asset transferred.",
    metadata={
        "from_employee_id": (
            str(from_employee.pk)
            if from_employee
            else None
        ),
        "from_employee_name": (
            from_employee.full_name
            if from_employee
            else None
        ),
        "from_site_id": (
            str(from_site.pk)
            if from_site
            else None
        ),
        "from_site_name": (
            from_site.name
            if from_site
            else None
        ),
        "to_employee_id": (
            str(to_employee.pk)
            if to_employee
            else None
        ),
        "to_employee_name": (
            to_employee.full_name
            if to_employee
            else None
        ),
        "to_site_id": (
            str(to_site.pk)
            if to_site
            else None
        ),
        "to_site_name": (
            to_site.name
            if to_site
            else None
        ),
        "reason": dto.reason or "",
    },
)

        # -------------------------------------------------
        # 9. Keep asset assigned
        # -------------------------------------------------

        if dto.asset.status != AssetStatus.ASSIGNED:

            dto.asset.status = AssetStatus.ASSIGNED

            dto.asset.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

        return transfer

    # =====================================================
    # Update Transfer
    # =====================================================

    @transaction.atomic
    def update(
        self,
        transfer: AssetTransfer,
        dto: AssetTransferUpdateDTO,
    ) -> AssetTransfer:

        self.validator.validate_update(
            transfer,
            dto,
        )

        update_data = {
            "transfer_date": dto.transfer_date,
            "reason": dto.reason,
            "remarks": dto.remarks,
            "is_active": dto.is_active,
        }

        return self.repository.update(
            transfer,
            **update_data,
        )

    # =====================================================
    # Get
    # =====================================================

    def get(
        self,
        pk,
    ) -> AssetTransfer:

        return self.repository.get(
            pk,
        )

    # =====================================================
    # List
    # =====================================================

    def list(
        self,
        query="",
        page=1,
    ):

        return self.repository.list(
            query=query,
            page=page,
        )