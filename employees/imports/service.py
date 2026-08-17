from django.db import transaction

from employees.dtos import EmployeeCreateDTO
from employees.services import EmployeeService

from .validator import EmployeeImportValidator


class EmployeeImportService:

    def __init__(self):
        self.validator = EmployeeImportValidator()
        self.employee_service = EmployeeService()

    def preview(self, rows):

        rows = list(rows)

        if not rows:
            return {
                "rows": [],
                "total": 0,
                "valid": 0,
                "errors": 0,
                "can_import": False,
            }

        self.validator.validate_headers(
            rows[0].keys()
        )

        results = []
        seen_employee_ids = set()

        for index, row in enumerate(
            rows,
            start=2,
        ):

            data = self.validator.validate_row(row)

            employee_id = data.get(
                "employee_id"
            )

            errors = list(
                data["errors"]
            )

            if (
                employee_id
                and employee_id in seen_employee_ids
            ):
                errors.append(
                    "Duplicate Employee ID in import file."
                )

            elif employee_id:
                seen_employee_ids.add(
                    employee_id
                )

            results.append({
                "row_number": index,
                "data": row,
                "employee_id": employee_id,
                "country": (
                    data["country"].name
                    if data["country"]
                    else None
                ),
                "site": (
                    data["site"].name
                    if data["site"]
                    else None
                ),
                "department": (
                    data["department"].name
                    if data["department"]
                    else None
                ),
                "job_title": (
                    data["job_title"].name
                    if data["job_title"]
                    else None
                ),
                "errors": errors,
                "valid": not errors,
            })

        valid = sum(
            1
            for row in results
            if row["valid"]
        )

        error_count = len(results) - valid

        return {
            "rows": results,
            "total": len(results),
            "valid": valid,
            "errors": error_count,
            "can_import": (
                len(results) > 0
                and error_count == 0
            ),
        }

    @transaction.atomic
    def import_rows(self, rows):

        preview = self.preview(rows)

        if not preview["can_import"]:
            raise ValueError(
                "Cannot import employees. "
                "Please correct the validation errors."
            )

        imported = []

        for row in rows:

            data = self.validator.validate_row(
                row
            )

            dto = EmployeeCreateDTO(
                country=data["country"],
                site=data["site"],
                department=data["department"],
                job_title=data["job_title"],
                manager=data["manager"],
                employee_id=data["employee_id"],
                first_name=data["first_name"],
                middle_name=data["middle_name"],
                last_name=data["last_name"],
                gender=data["gender"],
                joining_date=data["joining_date"],
                last_working_date=data[
                    "last_working_date"
                ],
                phone=data["phone"],
                email=data["email"],
                remarks=data["remarks"],
            )

            employee = (
                self.employee_service
                .create_employee(dto)
            )

            imported.append(employee)

        return imported