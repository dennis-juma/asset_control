
from __future__ import annotations
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from assets.choices.choices import AssignmentStatus, AssetStatus
from assets.choices.history_choices import AssetHistoryEvent
from assets.models import Asset, AssetAssignment
from assets.services.asset_history_service import AssetHistoryService
from assets.services.asset_service import AssetService
from employees.models import Employee
from datetime import date
from typing import Optional



class AssetAssignmentService:
    """
    Business logic for asset assignment operations.

    Responsibilities:
    - Assign assets
    - Return assets
    - Transfer assets
    - Maintain asset lifecycle
    - Record assignment history
    """

    @staticmethod
    @transaction.atomic
    def assign_asset(
        *,
        asset: Asset,
        employee: Employee,
        assigned_by: AbstractBaseUser,
        expected_return_date: Optional[date] = None,
        notes: str = "",
    ) -> AssetAssignment:
        """
        Assign an asset to an employee.
        """

        AssetAssignmentService._validate_asset_available(asset)

        assignment = AssetAssignment.objects.create(
            asset=asset,
            employee=employee,
            assigned_by=assigned_by,
            assigned_date=timezone.now(),
            expected_return_date=expected_return_date,
            status=AssignmentStatus.ACTIVE,
            notes=notes,
        )

        AssetService.change_status(
            asset=asset,
            new_status=AssetStatus.ASSIGNED,
            performed_by=assigned_by,
            employee=employee,
            notes="Asset assigned.",
        )

        AssetHistoryService.log_event(
            asset=asset,
            event_type=AssetHistoryEvent.ASSIGNED,
            performed_by=assigned_by,
            employee=employee,
            new_status=AssetStatus.ASSIGNED,
            notes=notes or "Asset assigned.",
        )

        return assignment
    
    @staticmethod
    def _validate_asset_available(asset: Asset) -> None:
        """
        Ensure the asset can be assigned.
        """

        if asset.status != AssetStatus.IN_STOCK:
            raise ValidationError(
                f"Asset '{asset.asset_tag}' is not available for assignment."
            )

        if AssetAssignment.objects.filter(
            asset=asset,
            status=AssignmentStatus.ACTIVE,
        ).exists():
            raise ValidationError(
                "Asset already has an active assignment."
            )
    @staticmethod
    @transaction.atomic
    def return_asset(
        *,
        assignment: AssetAssignment,
        returned_by: AbstractBaseUser,
        notes: str = "",
    ) -> AssetAssignment:
        """
        Return an assigned asset.

        This will:
        - Validate the assignment
        - Mark it as returned
        - Update the asset status
        - Record the history event
        """

        AssetAssignmentService._validate_active_assignment(assignment)

        assignment.status = AssignmentStatus.RETURNED
        assignment.returned_by = returned_by
        assignment.returned_date = timezone.now()

        assignment.full_clean()
        assignment.save()

        AssetService.change_status(
            asset=assignment.asset,
            new_status=AssetStatus.IN_STOCK,
            performed_by=returned_by,
            employee=assignment.employee,
            notes="Asset returned.",
        )

        AssetHistoryService.log_event(
            asset=assignment.asset,
            event_type=AssetHistoryEvent.RETURNED,
            performed_by=returned_by,
            employee=assignment.employee,
            old_status=AssetStatus.ASSIGNED,
            new_status=AssetStatus.IN_STOCK,
            notes=notes or "Asset returned.",
        )

        return assignment
    
    @staticmethod
    @transaction.atomic
    def transfer_asset(
        *,
        assignment: AssetAssignment,
        new_employee: Employee,
        transferred_by: AbstractBaseUser,
        expected_return_date: Optional[date] = None,
        notes: str = "",
    ) -> AssetAssignment:
        """
        Transfer an asset from one employee to another.
        """

        AssetAssignmentService._validate_active_assignment(assignment)

        if assignment.employee == new_employee:
            raise ValidationError(
                "The asset is already assigned to this employee."
            )

        asset = assignment.asset

        # Close current assignment
        AssetAssignmentService.return_asset(
            assignment=assignment,
            returned_by=transferred_by,
            notes=f"Transferred to {new_employee}.",
        )

        # Create the new assignment
        new_assignment = AssetAssignmentService.assign_asset(
            asset=asset,
            employee=new_employee,
            assigned_by=transferred_by,
            expected_return_date=expected_return_date,
            notes=notes or f"Transferred from {assignment.employee}.",
        )

        AssetHistoryService.log_event(
            asset=asset,
            event_type=AssetHistoryEvent.TRANSFERRED,
            performed_by=transferred_by,
            employee=new_employee,
            old_status=AssetStatus.ASSIGNED,
            new_status=AssetStatus.ASSIGNED,
            notes=notes or "Asset transferred.",
        )

        return new_assignment