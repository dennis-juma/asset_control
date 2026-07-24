from django.db import transaction
from django.core.exceptions import ValidationError

from assets.models import AssetAssignment
from assets.choices.choices import AssignmentStatus

class AssetTransferService:
    """
    Service responsible for transferring an asset
    from one employee to another.
    """

    @staticmethod
    @transaction.atomic
    def transfer(
        assignment: AssetAssignment,
        employee,
        assigned_by,
        assigned_date,
        expected_return_date=None,
        notes="",
    ):
        """
        Transfer an active assignment to another employee.

        Returns:
            AssetAssignment: Newly created assignment.
        """

        if assignment.status != AssignmentStatus.ACTIVE:
            raise ValidationError(
                "Only active assignments can be transferred."
            )

        if assignment.employee == employee:
            raise ValidationError(
                "Asset is already assigned to this employee."
            )

        new_assignment = assignment.transfer(
            employee=employee,
            assigned_by=assigned_by,
            assigned_date=assigned_date,
            expected_return_date=expected_return_date,
            notes=notes,
        )

        return new_assignment