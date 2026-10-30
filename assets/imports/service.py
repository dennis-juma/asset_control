from django.db import transaction

from assets.dtos.asset_assignment import AssetAssignmentCreateDTO
from assets.models import Asset
from assets.services import AssetAssignmentService
from .validator import AssetImportValidator, AssetAssignmentImportValidator


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

    def confirm(self, rows):
        return self.import_rows(rows)

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


class AssetAssignmentImportService:

    def __init__(self):
        self.validator = AssetAssignmentImportValidator()

    def preview(self, rows):
        rows = list(rows)

        results = []
        valid_count = 0
        error_count = 0

        for index, row in enumerate(rows, start=2):
            row = dict(row)
            errors = list(dict.fromkeys(
                self.validator.validate_row(row)
            ))

            is_valid = not errors
            if is_valid:
                valid_count += 1
            else:
                error_count += 1

            results.append(
                {
                    "row_number": index,
                    "data": row,
                    "asset": str(row.get("Asset Tag") or "").strip(),
                    "country": str(row.get("Country") or "").strip(),
                    "assignment_type": str(row.get("Assignment Type") or "").strip(),
                    "assigned_to": str(
                        row.get("Employee ID") or row.get("Employee Name") or row.get("Site Name") or ""
                    ).strip(),
                    "assigned_date": str(row.get("Assigned Date") or "").strip(),
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
                len(rows) > 0 and error_count == 0
            ),
        }

    @transaction.atomic
    def import_rows(self, rows, *, user=None):
        preview = self.preview(rows)

        if not preview["can_import"]:
            raise ValueError(
                "The import file contains validation errors."
            )

        imported = []
        service = AssetAssignmentService()

        for row in rows:
            country = self.validator._resolve_country(
                row.get("Country")
            )
            asset = self.validator._resolve_asset(
                row.get("Asset Tag"),
                country,
            )
            assignment_type = self.validator._parse_assignment_type(
                row.get("Assignment Type")
            )
            employee = None
            site = None

            if assignment_type.value == "EMPLOYEE":
                employee = self.validator._resolve_employee(
                    row.get("Employee ID"),
                    row.get("Employee Name"),
                    country,
                )
            elif assignment_type.value == "SITE":
                site = self.validator._resolve_site(
                    row.get("Site Name"),
                    country,
                )

            assigned_date, _ = self.validator._parse_date(
                row.get("Assigned Date")
            )
            expected_return_date, _ = self.validator._parse_date(
                row.get("Expected Return Date")
            )

            dto = AssetAssignmentCreateDTO(
                country=country,
                asset=asset,
                assignment_type=assignment_type,
                employee=employee,
                site=site,
                assigned_date=assigned_date,
                expected_return_date=expected_return_date,
                remarks=self.validator._text(row.get("Remarks")),
            )

            imported.append(service.create(dto, user=user))

        return imported
