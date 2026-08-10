from django.core.exceptions import ValidationError

from assets.choices import (
    AssignmentStatus,
    AssetStatus,
)

from assets.dtos.asset_transfer import (
    AssetTransferCreateDTO,
    AssetTransferUpdateDTO,
)


class AssetTransferValidator:

    # =====================================================
    # Public Validators
    # =====================================================

    def validate_create(
        self,
        dto: AssetTransferCreateDTO,
    ) -> None:

        self._validate_asset_assigned(dto)

        self._validate_source_assignment(dto)

        self._validate_transfer_target(dto)

        self._validate_transfer_date(dto)

        self._validate_same_target(dto)

    def validate_update(
        self,
        transfer,
        dto: AssetTransferUpdateDTO,
    ) -> None:

        self._validate_update_transfer_date(
            transfer,
            dto,
        )

    # =====================================================
    # Asset Validation
    # =====================================================

    def _validate_asset_assigned(
        self,
        dto,
    ) -> None:

        if dto.asset.status != AssetStatus.ASSIGNED:

            raise ValidationError(
                {
                    "asset":
                    "Only assigned assets can be transferred."
                }
            )

    # =====================================================
    # Current Assignment
    # =====================================================

    def _validate_source_assignment(
        self,
        dto,
    ) -> None:

        assignment = dto.previous_assignment

        if assignment is None:

            raise ValidationError(
                {
                    "asset":
                    "This asset does not have an active assignment."
                }
            )

        if assignment.status != AssignmentStatus.ACTIVE:

            raise ValidationError(
                {
                    "asset":
                    "The selected assignment is not active."
                }
            )

        if assignment.asset_id != dto.asset.pk:

            raise ValidationError(
                {
                    "asset":
                    "The assignment does not belong to this asset."
                }
            )

    # =====================================================
    # Transfer Target
    # =====================================================

    def _validate_transfer_target(
        self,
        dto,
    ) -> None:

        employee_selected = (
            dto.to_employee is not None
        )

        site_selected = (
            dto.to_site is not None
        )

        # Exactly one target must be selected.
        if employee_selected == site_selected:

            raise ValidationError(
                {
                    "to_employee":
                    "Select either an Employee or a Site."
                }
            )

        # -------------------------------------------------
        # Employee Target
        # -------------------------------------------------

        if employee_selected:

            employee = dto.to_employee

            if not employee.is_active:

                raise ValidationError(
                    {
                        "to_employee":
                        "Selected employee is inactive."
                    }
                )

            if employee.company_id != dto.company.pk:

                raise ValidationError(
                    {
                        "to_employee":
                        "Selected employee belongs to another company."
                    }
                )

            if not employee.site:

                raise ValidationError(
                    {
                        "to_employee":
                        "Selected employee does not have an assigned site."
                    }
                )

        # -------------------------------------------------
        # Site Target
        # -------------------------------------------------

        if site_selected:

            site = dto.to_site

            if not site.is_active:

                raise ValidationError(
                    {
                        "to_site":
                        "Selected site is inactive."
                    }
                )

            if site.company_id != dto.company.pk:

                raise ValidationError(
                    {
                        "to_site":
                        "Selected site belongs to another company."
                    }
                )

    # =====================================================
    # Same Target
    # =====================================================

    def _validate_same_target(
        self,
        dto,
    ) -> None:

        assignment = dto.previous_assignment

        if assignment is None:
            return

        # Employee → same employee
        if (
            dto.to_employee is not None
            and assignment.employee_id is not None
            and dto.to_employee.pk
            == assignment.employee_id
        ):

            raise ValidationError(
                {
                    "to_employee":
                    "The asset is already assigned to this employee."
                }
            )

        # Site → same site
        if (
            dto.to_site is not None
            and assignment.site_id is not None
            and dto.to_site.pk
            == assignment.site_id
        ):

            raise ValidationError(
                {
                    "to_site":
                    "The asset is already assigned to this site."
                }
            )

    # =====================================================
    # Create Transfer Date
    # =====================================================

    def _validate_transfer_date(
        self,
        dto,
    ) -> None:

        if dto.transfer_date is None:

            raise ValidationError(
                {
                    "transfer_date":
                    "Transfer Date is required."
                }
            )

        assignment = dto.previous_assignment

        if (
            assignment is not None
            and assignment.assigned_date is not None
            and dto.transfer_date
            < assignment.assigned_date
        ):

            raise ValidationError(
                {
                    "transfer_date":
                    "Transfer Date cannot be earlier than the "
                    "original Assignment Date."
                }
            )

    # =====================================================
    # Update Transfer Date
    # =====================================================

    def _validate_update_transfer_date(
        self,
        transfer,
        dto,
    ) -> None:

        if dto.transfer_date is None:

            raise ValidationError(
                {
                    "transfer_date":
                    "Transfer Date is required."
                }
            )

        previous_assignment = (
            transfer.previous_assignment
        )

        if (
            previous_assignment is not None
            and previous_assignment.assigned_date is not None
            and dto.transfer_date
            < previous_assignment.assigned_date
        ):

            raise ValidationError(
                {
                    "transfer_date":
                    "Transfer Date cannot be earlier than the "
                    "original Assignment Date."
                }
            )