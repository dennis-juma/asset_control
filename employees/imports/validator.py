from datetime import date
from django.core.exceptions import ValidationError

from common.choices import Gender

from employees.dtos import EmployeeCreateDTO
from employees.models import Employee
from organizations.models import (
    Country,
    Site,
    Department,
    JobTitle,
)


class EmployeeImportValidator:

    REQUIRED_COLUMNS = (
        "Country",
        "Site",
        "Department",
        "Job Title",
        "Employee ID",
        "First Name",
        "Last Name",
        "Gender",
        "Joining Date",
    )

    OPTIONAL_COLUMNS = (
        "Manager",
        "Middle Name",
        "Last Working Date",
        "Phone",
        "Email",
        "Remarks",
    )

    ALL_COLUMNS = REQUIRED_COLUMNS + OPTIONAL_COLUMNS

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
                "Missing required columns: "
                + ", ".join(missing)
            )

    def validate_row(self, row):
        errors = []

        country = self._resolve_country(
            row.get("Country"),
            errors,
        )

        site = self._resolve_site(
            row.get("Site"),
            country,
            errors,
        )

        department = self._resolve_department(
            row.get("Department"),
            country,
            errors,
        )

        job_title = self._resolve_job_title(
            row.get("Job Title"),
            country,
            department,
            errors,
        )

        manager = self._resolve_manager(
            row.get("Manager"),
            country,
            errors,
        )

        employee_id = self._text(
            row.get("Employee ID")
        )

        first_name = self._text(
            row.get("First Name")
        )

        middle_name = self._text(
            row.get("Middle Name")
        )

        last_name = self._text(
            row.get("Last Name")
        )

        gender = self._parse_gender(
            row.get("Gender")
        )

        joining_date = self._parse_date(
            row.get("Joining Date"),
            "Joining Date",
            errors,
        )

        last_working_date = self._parse_date(
            row.get("Last Working Date"),
            "Last Working Date",
            errors,
        )

        phone = self._text(row.get("Phone"))
        email = self._text(row.get("Email"))
        remarks = self._text(row.get("Remarks"))

        if not employee_id:
            errors.append("Employee ID is required.")
        elif Employee.objects.filter(
            employee_id=employee_id
        ).exists():
            errors.append(
                f"Employee ID '{employee_id}' already exists."
            )

        if not first_name:
            errors.append("First Name is required.")

        if not last_name:
            errors.append("Last Name is required.")

        if gender is None:
            errors.append("Gender is invalid.")

        if country and site:
            if site.country_id != country.id:
                errors.append(
                    "Site does not belong to the selected country."
                )

        if (
            country
            and department
            and department.country_id
            and department.country_id != country.id
        ):
            errors.append(
                "Department does not belong to the selected country."
            )



        if (
            country
            and job_title
            and job_title.country_id
            and job_title.country_id != country.id
        ):
            errors.append(
                "Job Title does not belong to the selected country."
            )

        if (
            department
            and job_title
            and job_title.department_id
            and job_title.department_id != department.id
        ):
            errors.append(
                "Job Title does not belong to the selected department."
            )

        if (
            joining_date
            and last_working_date
            and last_working_date < joining_date
        ):
            errors.append(
                "Last working date cannot be earlier than joining date."
            )

        if email:
            from django.core.validators import validate_email

            try:
                validate_email(email)
            except ValidationError:
                errors.append("Email address is invalid.")

        return {
            "errors": errors,
            "country": country,
            "site": site,
            "department": department,
            "job_title": job_title,
            "manager": manager,
            "employee_id": employee_id,
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "gender": gender,
            "joining_date": joining_date,
            "last_working_date": last_working_date,
            "phone": phone,
            "email": email,
            "remarks": remarks,
        }

    def _resolve_country(self, value, errors):
        value = self._text(value)

        if not value:
            errors.append("Country is required.")
            return None

        queryset = Country.objects.all()

        country = (
            queryset.filter(name__iexact=value).first()
            or queryset.filter(iso2__iexact=value).first()
            or queryset.filter(iso3__iexact=value).first()
            or queryset.filter(code__iexact=value).first()
        )

        if not country:
            errors.append(
                f"Country '{value}' was not found."
            )

        return country

    def _resolve_site(self, value, country, errors):
        value = self._text(value)

        if not value:
            errors.append("Site is required.")
            return None

        queryset = Site.objects.all()

        if country:
            queryset = queryset.filter(
                country=country
            )

        site = (
            queryset.filter(name__iexact=value).first()
            or queryset.filter(code__iexact=value).first()
        )

        if not site:
            errors.append(
                f"Site '{value}' was not found."
            )

        return site

    def _resolve_department(
        self,
        value,
        country,
        errors,
    ):
        value = self._text(value)

        if not value:
            errors.append("Department is required.")
            return None

        queryset = Department.objects.all()

        if country:
            queryset = queryset.filter(
                country=country
            )

        

        department = (
            queryset.filter(name__iexact=value).first()
            or queryset.filter(code__iexact=value).first()
        )

        if not department:
            errors.append(
                f"Department '{value}' was not found."
            )

        return department

    def _resolve_job_title(
        self,
        value,
        country,
        department,
        errors,
    ):
        value = self._text(value)

        if not value:
            errors.append("Job Title is required.")
            return None

        queryset = JobTitle.objects.all()

        if country:
            queryset = queryset.filter(
                country=country
            )

        if department:
            queryset = queryset.filter(
                department=department
            )

        job_title = (
            queryset.filter(name__iexact=value).first()
            or queryset.filter(code__iexact=value).first()
        )

        if not job_title:
            errors.append(
                f"Job Title '{value}' was not found."
            )

        return job_title

    def _resolve_manager(
        self,
        value,
        country,
        errors,
    ):
        value = self._text(value)

        if not value:
            return None

        queryset = Employee.objects.all()

        if country:
            queryset = queryset.filter(
                country=country
            )

        manager = queryset.filter(
            employee_id__iexact=value
        ).first()

        if not manager:
            errors.append(
                f"Manager '{value}' was not found."
            )

        return manager

    def _parse_gender(self, value):
        value = self._text(value)

        if not value:
            return None

        for choice_value, label in Gender.choices:

            if value.upper() == choice_value.upper():
                return choice_value

            if value.casefold() == label.casefold():
                return choice_value

        return None

    def _parse_date(
        self,
        value,
        field_name,
        errors,
    ):
        if value in (None, ""):
            if field_name == "Joining Date":
                errors.append(
                    "Joining Date is required."
                )
            return None

        if isinstance(value, date):
            return value

        value = self._text(value)

        for fmt in (
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%d-%m-%Y",
        ):
            try:
                from datetime import datetime

                return datetime.strptime(
                    value,
                    fmt,
                ).date()

            except ValueError:
                continue

        errors.append(
            f"{field_name}: Invalid date. "
            "Use YYYY-MM-DD."
        )

        return None

    @staticmethod
    def _text(value):
        if value is None:
            return ""

        return str(value).strip()