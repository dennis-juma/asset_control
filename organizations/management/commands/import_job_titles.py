import csv

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from organizations.models import Department, JobTitle


class Command(BaseCommand):
    help = "Bulk import job titles with departments from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            "file",
            help="Path to CSV file.",
        )

        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Validate the import without saving changes.",
        )

        parser.add_argument(
            "--update",
            action="store_true",
            help="Update existing job titles with the CSV department.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        file_path = options["file"]
        dry_run = options["dry_run"]
        update_existing = options["update"]

        try:
            with open(
                file_path,
                "r",
                encoding="utf-8-sig",
                newline="",
            ) as file:

                reader = csv.DictReader(file)

                if not reader.fieldnames:
                    raise CommandError("CSV file has no header.")

                required_columns = {"Department", "name"}

                missing_columns = required_columns - set(reader.fieldnames)

                if missing_columns:
                    raise CommandError(
                        "Missing required column(s): "
                        + ", ".join(sorted(missing_columns))
                    )

                created = 0
                updated = 0
                skipped = 0
                empty = 0
                missing_departments = 0
                ambiguous_departments = 0

                missing_department_names = set()
                ambiguous_department_names = set()

                for row_number, row in enumerate(reader, start=2):

                    department_name = (
                        row.get("Department") or ""
                    ).strip()

                    job_title_name = (
                        row.get("name") or ""
                    ).strip()

                    if not department_name or not job_title_name:
                        empty += 1
                        continue

                    # Find active, non-deleted department.
                    departments = list(
                        Department.objects.filter(
                            name__iexact=department_name,
                            is_deleted=False,
                            is_active=True,
                        )
                    )

                    if not departments:
                        missing_departments += 1
                        missing_department_names.add(
                            department_name
                        )

                        self.stdout.write(
                            self.style.WARNING(
                                f"Row {row_number}: "
                                f"Department not found: "
                                f"{department_name}"
                            )
                        )

                        continue

                    if len(departments) > 1:
                        ambiguous_departments += 1
                        ambiguous_department_names.add(
                            department_name
                        )

                        self.stdout.write(
                            self.style.WARNING(
                                f"Row {row_number}: "
                                f"Multiple departments found: "
                                f"{department_name}"
                            )
                        )

                        continue

                    department = departments[0]

                    # A JobTitle belongs to a department.
                    job_title = (
                        JobTitle.objects
                        .filter(
                            name__iexact=job_title_name,
                            department=department,
                            is_deleted=False,
                        )
                        .first()
                    )

                    if job_title:

                        if update_existing:
                            job_title.name = job_title_name
                            job_title.department = department
                            job_title.save()

                            updated += 1

                        else:
                            skipped += 1

                        continue

                    JobTitle.objects.create(
                        name=job_title_name,
                        department=department,
                        description="",
                    )

                    created += 1

                    self.stdout.write(
                        f"Added: "
                        f"{department.name} → "
                        f"{job_title_name}"
                    )

                if dry_run:
                    transaction.set_rollback(True)

        except FileNotFoundError:
            raise CommandError(
                f"File not found: {file_path}"
            )

        except UnicodeDecodeError:
            raise CommandError(
                "Could not read the CSV file as UTF-8."
            )

        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write(
            self.style.SUCCESS(
                "Import completed"
            )
        )
        self.stdout.write("=" * 60)

        self.stdout.write(
            f"Created:              {created}"
        )

        self.stdout.write(
            f"Updated:              {updated}"
        )

        self.stdout.write(
            f"Skipped:              {skipped}"
        )

        self.stdout.write(
            f"Empty rows:           {empty}"
        )

        self.stdout.write(
            f"Missing departments:  {missing_departments}"
        )

        self.stdout.write(
            f"Ambiguous departments:{ambiguous_departments}"
        )

        if missing_department_names:
            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING(
                    "Missing departments:"
                )
            )

            for name in sorted(missing_department_names):
                self.stdout.write(
                    f"  - {name}"
                )

        if ambiguous_department_names:
            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING(
                    "Ambiguous departments:"
                )
            )

            for name in sorted(ambiguous_department_names):
                self.stdout.write(
                    f"  - {name}"
                )

        if dry_run:
            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING(
                    "DRY RUN: No changes were saved."
                )
            )