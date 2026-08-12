from django.core.exceptions import ValidationError

from assets.dtos import (
    AssetCreateDTO,
    AssetUpdateDTO,
)

from assets.repositories import AssetRepository


class AssetValidator:

    def __init__(self):
        self.repository = AssetRepository()

    # =====================================================
    # Public Validators
    # =====================================================

    def validate_create(
        self,
        dto: AssetCreateDTO,
    ):
        self._validate_serial_number(
            dto.serial_number,
        )
        self._validate_asset_model(dto)
        self._validate_company(dto)
        self._validate_purchase_dates(dto)
        self._validate_purchase_cost(dto)

    def validate_update(
        self,
        asset,
        dto: AssetUpdateDTO,
    ):
        self._validate_serial_number(
            dto.serial_number,
            exclude_pk=asset.pk,
        )

        self._validate_asset_model(dto)
        self._validate_company(dto)
        self._validate_purchase_dates(dto)
        self._validate_purchase_cost(dto)

    # =====================================================
    # Private Validators
    # =====================================================

    def _validate_serial_number(
        self,
        serial_number,
        exclude_pk=None,
    ):
        if self.repository.exists_serial_number(
            serial_number,
            exclude_pk,
        ):
            raise ValidationError(
                {
                    "serial_number":
                    "An asset with this Serial Number already exists."
                }
            )

    def _validate_asset_model(
        self,
        dto,
    ):
        if not dto.asset_model.is_active:
            raise ValidationError(
                {
                    "asset_model":
                    "Selected Asset Model is inactive."
                }
            )

    def _validate_company(
        self,
        dto,
    ):
        if dto.asset_model.country != dto.country:
            raise ValidationError(
                {
                    "country":
                    "Selected Asset Model belongs to another country."
                }
            )

    def _validate_purchase_dates(
        self,
        dto,
    ):
        if (
            dto.purchase_date
            and dto.received_date
            and dto.received_date < dto.purchase_date
        ):
            raise ValidationError(
                {
                    "received_date":
                    "Received Date cannot be earlier than Purchase Date."
                }
            )

    def _validate_purchase_cost(
        self,
        dto,
    ):
        if (
            dto.purchase_cost is not None
            and dto.purchase_cost < 0
        ):
            raise ValidationError(
                {
                    "purchase_cost":
                    "Purchase Cost cannot be negative."
                }
            )