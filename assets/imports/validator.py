from datetime import date
from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError

from assets.choices import AssetCondition
from assets.dtos import AssetCreateDTO
from assets.models import AssetModel
from organizations.models import Country
from assets.validators import AssetValidator


class AssetImportValidator:

    REQUIRED_COLUMNS = (
        "Country",
        "Asset Model",
        "Serial Number",
    )

    OPTIONAL_COLUMNS = (
        "Purchase Date",
        "Received Date",
        "Purchase Cost",
        "Invoice Number",
        "Condition",
        "Remarks",
    )

    ALL_COLUMNS = REQUIRED_COLUMNS + OPTIONAL_COLUMNS

    def __init__(self):
        self.asset_validator = AssetValidator()

    def validate_headers(self, headers):
        headers = {
            str(header).strip()
            for header in headers
            if header
        }

        missing = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in headers
        ]

        if missing:
            raise ValidationError(
                {
                    "headers": (
                        "Missing required columns: "
                        + ", ".join(missing)
                    )
                }
            )

    def validate_row(self, row):
        errors = []

        try:
            country = self._resolve_country(
                row.get("Country")
            )
        except ValidationError as exc:
            errors.append(str(exc))
            country = None

        try:
            asset_model = self._resolve_asset_model(
                row.get("Asset Model"),
                country,
            )
        except ValidationError as exc:
            errors.append(str(exc))
            asset_model = None

        serial_number = self._text(
            row.get("Serial Number")
        )

        if not serial_number:
            errors.append(
                "Serial Number is required."
            )

        purchase_date, error = self._parse_date(
            row.get("Purchase Date")
        )

        if error:
            errors.append(
                f"Purchase Date: {error}"
            )

        received_date, error = self._parse_date(
            row.get("Received Date")
        )

        if error:
            errors.append(
                f"Received Date: {error}"
            )

        purchase_cost, error = self._parse_decimal(
            row.get("Purchase Cost")
        )

        if error:
            errors.append(
                f"Purchase Cost: {error}"
            )

        condition = self._parse_condition(
            row.get("Condition")
        )

        if condition is None and self._text(
            row.get("Condition")
        ):
            errors.append(
                "Condition is invalid."
            )

        if country and asset_model and serial_number:
            dto = AssetCreateDTO(
                country=country,
                asset_model=asset_model,
                serial_number=serial_number,
                purchase_date=purchase_date,
                received_date=received_date,
                purchase_cost=purchase_cost,
                invoice_number=self._text(
                    row.get("Invoice Number")
                ),
                condition=condition or "",
                remarks=self._text(
                    row.get("Remarks")
                ),
            )

            try:
                self.asset_validator.validate_create(
                    dto
                )
            except ValidationError as exc:
                errors.extend(
                    self._validation_messages(exc)
                )

        return errors

    def _resolve_country(self, value):
        value = self._text(value)

        if not value:
            raise ValidationError(
                "Country is required."
            )

        country = Country.objects.filter(
            name__iexact=value
        ).first()

        if country:
            return country

        country = Country.objects.filter(
            iso2__iexact=value
        ).first()

        if country:
            return country

        country = Country.objects.filter(
            iso3__iexact=value
        ).first()

        if country:
            return country

        country = Country.objects.filter(
            code__iexact=value
        ).first()

        if country:
            return country

        raise ValidationError(
            f"Country '{value}' was not found."
        )

    def _resolve_asset_model(
        self,
        value,
        country,
    ):
        value = self._text(value)

        if not value:
            raise ValidationError(
                "Asset Model is required."
            )

        queryset = AssetModel.objects.select_related(
            "country",
            "brand",
        )

        if country:
            queryset = queryset.filter(
                country=country
            )

        model = queryset.filter(
            code__iexact=value
        ).first()

        if model:
            return self._validate_model(
                model,
                country,
            )

        models = queryset.filter(
            name__iexact=value
        )

        if models.count() == 1:
            return self._validate_model(
                models.first(),
                country,
            )

        if models.count() > 1:
            raise ValidationError(
                f"Asset Model '{value}' is ambiguous."
            )

        raise ValidationError(
            f"Asset Model '{value}' was not found."
        )

    def _validate_model(
        self,
        asset_model,
        country,
    ):
        if not asset_model.is_active:
            raise ValidationError(
                "Selected Asset Model is inactive."
            )

        if country and asset_model.country_id != country.id:
            raise ValidationError(
                "Selected Asset Model belongs to another country."
            )

        return asset_model

    def _parse_date(self, value):
        if value in (None, ""):
            return None, None

        if isinstance(value, date):
            return value, None

        value = self._text(value)

        for fmt in (
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%d-%m-%Y",
        ):
            try:
                return date.fromisoformat(
                    date.strptime(value, fmt).isoformat()
                ), None
            except ValueError:
                continue

        return None, "Invalid date. Use YYYY-MM-DD."

    def _parse_decimal(self, value):
        if value in (None, ""):
            return None, None

        try:
            return Decimal(
                str(value).replace(",", "").strip()
            ), None

        except (InvalidOperation, ValueError):
            return None, "Invalid number."

    def _parse_condition(self, value):
        value = self._text(value)

        if not value:
            return ""

        for choice_value, label in AssetCondition.choices:
            if value.upper() == choice_value:
                return choice_value

            if value.casefold() == label.casefold():
                return choice_value

        return None

    @staticmethod
    def _text(value):
        if value is None:
            return ""

        return str(value).strip()

    @staticmethod
    def _validation_messages(exc):
        messages = []

        if hasattr(exc, "message_dict"):
            for field_messages in exc.message_dict.values():
                for message in field_messages:
                    if isinstance(message, (list, tuple)):
                        messages.extend(
                            str(item)
                            for item in message
                        )
                    else:
                        messages.append(str(message))
        else:
            messages.extend(
                str(message)
                for message in exc.messages
            )

        return messages