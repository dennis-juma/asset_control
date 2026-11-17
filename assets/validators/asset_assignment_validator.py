from django.core.exceptions import ValidationError

from assets.choices import (
    AssetStatus,
    AssignmentStatus,
)
from assets.dtos import (
    AssetAssignmentCreateDTO,
    AssetAssignmentUpdateDTO,
)
from assets.repositories import (
    AssetAssignmentRepository,
)


class AssetAssignmentValidator:

    def __init__(self):
        self.repository = AssetAssignmentRepository()

    # =====================================================
    # Public Validators
    # =====================================================

    def validate_create(
        self,
        dto: AssetAssignmentCreateDTO,
    ):

        self._validate_asset_available(dto)
        self._validate_assignment_target(dto)
        self._validate_expected_return_date(dto)
        self._validate_active_assignment(dto)
        self._validate_employee_category_assignment(dto)

    def validate_update(
        self,
        assignment,
        dto: AssetAssignmentUpdateDTO,
    ):

        self._validate_assignment_target(dto)
        self._validate_expected_return_date(dto)

    # =====================================================
    # Private Validators
    # =====================================================

    def _validate_asset_available(
        self,
        dto,
    ):

        if dto.asset.status != AssetStatus.AVAILABLE:
            raise ValidationError(
                {
                    "asset":
                    "Only available assets can be assigned."
                }
            )

    def _validate_assignment_target(
    self,
    dto,
):

    # Employee assignment
        if dto.employee:

            if not dto.employee.is_active:
                raise ValidationError(
                    {
                        "employee":
                        "Selected employee is inactive."
                    }
                )

            return

        # Site assignment
        if dto.site:

            if not dto.site.is_active:
                raise ValidationError(
                    {
                        "site":
                        "Selected site is inactive."
                    }
                )

            return

        raise ValidationError(
            {
                "employee":
                "Select an Employee or a Site."
            }
        )


    def _validate_expected_return_date(
        self,
        dto,
    ):

        if (
            dto.expected_return_date
            and dto.assigned_date
            and dto.expected_return_date < dto.assigned_date
        ):
            raise ValidationError(
                {
                    "expected_return_date":
                    "Expected Return Date cannot be earlier than Assigned Date."
                }
            )

    def _validate_active_assignment(
        self,
        dto,
    ):

        if self.repository.has_active_assignment(dto.asset):
            raise ValidationError(
                {
                    "asset":
                    "This asset already has an active assignment."
                }
            )

    def _validate_employee_category_assignment(self, dto):
        # Category limits apply to employee assignments; site assignments are shared inventory.
        if not dto.employee or not dto.asset.asset_model or not dto.asset.asset_model.category:
            return

        existing = self.repository.active_assignment_in_category(
            dto.employee,
            dto.asset.asset_model.category,
        )
        if existing:
            category_name = dto.asset.asset_model.category.name
            raise ValidationError({
                "employee": (
                    f"{dto.employee.full_name} already has an active {category_name} asset "
                    f"({existing.asset.asset_tag}). Return it before assigning another."
                )
            })
