from django.db import transaction

from assets.models import Asset
from .validator import AssetImportValidator


class AssetImportService:

    def __init__(self):
        self.validator = AssetImportValidator()

    def preview(self, rows):
        rows = list(rows)

        results = []
        valid_count = 0
        error_count = 0

        seen_serial_numbers = set()

        for index, row in enumerate(rows, start=2):

            row = dict(row)

            errors = []

            serial_number = str(
                row.get("Serial Number") or ""
            ).strip()

            # Check duplicate serial numbers inside
            # the same import file.
            if serial_number:

                normalized_serial = serial_number.casefold()

                if normalized_serial in seen_serial_numbers:
                    errors.append(
                        "Duplicate Serial Number in import file."
                    )
                else:
                    seen_serial_numbers.add(
                        normalized_serial
                    )

            # Validate row using the existing validator.
            errors.extend(
                self.validator.validate_row(row)
            )

            # Remove duplicate error messages.
            errors = list(dict.fromkeys(errors))

            is_valid = not errors

            if is_valid:
                valid_count += 1
            else:
                error_count += 1

            results.append(
                {
                    "row_number": index,

                    "data": row,

                    # Prepared values for the template.
                    # This avoids dictionary keys containing
                    # spaces such as "Serial Number".
                    "serial_number": serial_number,

                    "country": str(
                        row.get("Country") or ""
                    ).strip(),

                    "asset_model": str(
                        row.get("Asset Model") or ""
                    ).strip(),

                    "errors": errors,

                    "valid": is_valid,
                }
            )

        return {
            "rows": results,
            "total": len(rows),
            "valid": valid_count,
            "errors": error_count,
            "can_import": (
                len(rows) > 0
                and error_count == 0
            ),
        }

    @transaction.atomic
    def import_rows(self, rows):

        preview = self.preview(rows)

        if not preview["can_import"]:
            raise ValueError(
                "The import file contains validation errors."
            )

        imported = []

        for row in rows:

            country = self.validator._resolve_country(
                row.get("Country")
            )

            asset_model = (
                self.validator._resolve_asset_model(
                    row.get("Asset Model"),
                    country,
                )
            )

            serial_number = self.validator._text(
                row.get("Serial Number")
            )

            purchase_date, _ = (
                self.validator._parse_date(
                    row.get("Purchase Date")
                )
            )

            received_date, _ = (
                self.validator._parse_date(
                    row.get("Received Date")
                )
            )

            purchase_cost, _ = (
                self.validator._parse_decimal(
                    row.get("Purchase Cost")
                )
            )

            condition = (
                self.validator._parse_condition(
                    row.get("Condition")
                )
                or ""
            )

            asset = Asset.objects.create(
                country=country,
                asset_model=asset_model,
                serial_number=serial_number,
                purchase_date=purchase_date,
                received_date=received_date,
                purchase_cost=purchase_cost,
                invoice_number=self.validator._text(
                    row.get("Invoice Number")
                ),
                condition=condition,
                remarks=self.validator._text(
                    row.get("Remarks")
                ),
            )

            imported.append(asset)

        return imported