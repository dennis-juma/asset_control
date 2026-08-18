from django.core.management.base import BaseCommand, CommandError

from core.imports.enums import ImportType
from core.imports.service import ImportService
from employees.imports import EmployeeImportService


class Command(BaseCommand):
    help = "Bulk import employees from CSV or XLSX."

    def add_arguments(self, parser):
        parser.add_argument(
            "file",
            help="Path to CSV or XLSX file.",
        )

        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Validate the file without saving employees.",
        )

    def handle(self, *args, **options):
        file_path = options["file"]
        dry_run = options["dry_run"]

        try:
            with open(file_path, "rb") as uploaded_file:

                filename = file_path.lower()

                if filename.endswith(".csv"):
                    import_type = ImportType.CSV

                elif filename.endswith(".xlsx"):
                    import_type = ImportType.EXCEL

                else:
                    raise CommandError(
                        "Only CSV and XLSX files are supported."
                    )

                rows = ImportService.import_file(
                    uploaded_file,
                    import_type,
                )

        except FileNotFoundError:
            raise CommandError(
                f"File not found: {file_path}"
            )

        except Exception as exc:
            raise CommandError(
                f"Unable to read import file: {exc}"
            )

        service = EmployeeImportService()

        try:
            result = service.preview(rows)

        except Exception as exc:
            raise CommandError(
                f"Validation failed: {exc}"
            )

        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write(
            self.style.SUCCESS("Employee Import Preview")
        )
        self.stdout.write("=" * 60)

        self.stdout.write(
            f"Total rows:       {result['total']}"
        )

        self.stdout.write(
            f"Valid rows:       {result['valid']}"
        )

        self.stdout.write(
            f"Rows with errors: {result['errors']}"
        )

        self.stdout.write("")

        # Display validation errors
        for row in result["rows"]:
            if row["errors"]:
                self.stdout.write(
                    self.style.ERROR(
                        f"Row {row['row_number']}: "
                        + "; ".join(row["errors"])
                    )
                )

        if not result["can_import"]:
            self.stdout.write("")
            self.stdout.write(
                self.style.ERROR(
                    "Import cannot proceed. "
                    "Fix the validation errors first."
                )
            )
            return

        if dry_run:
            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING(
                    "DRY RUN: No employees were imported."
                )
            )
            return

        try:
            employees = service.import_rows(rows)

        except Exception as exc:
            raise CommandError(
                f"Employee import failed: {exc}"
            )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"{len(employees)} employee(s) "
                "imported successfully."
            )
        )