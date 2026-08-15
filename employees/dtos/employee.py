from dataclasses import dataclass
from datetime import date
from typing import Any
from accounts.models.choices import UserType

from employees.models.employee import Employee
from organizations.models import (
    Country,
    Department,
    JobTitle,
    Site,
)


@dataclass
class EmployeeCreateDTO:
    """
    Data Transfer Object for creating an employee.
    """

    country: Country
    site: Site
    department: Department
    job_title: JobTitle

    employee_id: str

    first_name: str
    middle_name: str
    last_name: str

    gender: str

    joining_date: date
    last_working_date: date | None = None

    phone: str = ""
    email: str = ""

    manager: "Employee | None" = None

    photo: Any | None = None

    remarks: str = ""


@dataclass
class EmployeeUpdateDTO:
    """
    Data Transfer Object for updating an employee.
    """

    country: Country
    site: Site
    department: Department
    job_title: JobTitle

    employee_id: str

    first_name: str
    middle_name: str
    last_name: str

    gender: str

    joining_date: date
    last_working_date: date | None = None

    phone: str = ""
    email: str = ""

    manager: "Employee | None" = None

    photo: Any | None = None

    remarks: str = ""

    is_active: bool = True
    system_role: str = UserType.USER