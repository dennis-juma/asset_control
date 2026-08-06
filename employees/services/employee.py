from django.core.exceptions import ValidationError

from employees.dtos import (
    EmployeeCreateDTO,
    EmployeeUpdateDTO,
)
from employees.models import Employee
from employees.repositories import EmployeeRepository


class EmployeeService:

    def __init__(self):
        self.repository = EmployeeRepository()

    def create_employee(
        self,
        dto: EmployeeCreateDTO,
    ) -> Employee:

        self._validate_dates(
            dto.joining_date,
            dto.last_working_date,
        )

        employee = Employee(
            company=dto.company,
            site=dto.site,
            department=dto.department,
            job_title=dto.job_title,
            manager=dto.manager,
            employee_id=dto.employee_id,
            first_name=dto.first_name,
            middle_name=dto.middle_name,
            last_name=dto.last_name,
            gender=dto.gender,
            joining_date=dto.joining_date,
            last_working_date=dto.last_working_date,
            phone=dto.phone,
            email=dto.email,
            photo=dto.photo,
            user=dto.user,
            remarks=dto.remarks,
        )

        employee.full_clean()

        return self.repository.create(employee)

    def update_employee(
        self,
        employee: Employee,
        dto: EmployeeUpdateDTO,
    ) -> Employee:

        self._validate_dates(
            dto.joining_date,
            dto.last_working_date,
        )

        employee.company = dto.company
        employee.site = dto.site
        employee.department = dto.department
        employee.job_title = dto.job_title
        employee.manager = dto.manager
        employee.employee_id = dto.employee_id
        employee.first_name = dto.first_name
        employee.middle_name = dto.middle_name
        employee.last_name = dto.last_name
        employee.gender = dto.gender
        employee.joining_date = dto.joining_date
        employee.last_working_date = dto.last_working_date
        employee.phone = dto.phone
        employee.email = dto.email
        employee.photo = dto.photo
        employee.user = dto.user
        employee.remarks = dto.remarks
        employee.is_active = dto.is_active

        self._validate_manager(employee)

        employee.full_clean()

        return self.repository.update(employee)

    def delete(
        self,
        employee: Employee,
    ):
        self.repository.delete(employee)

    def _validate_dates(
        self,
        joining_date,
        last_working_date,
    ):
        """
        Last working date cannot be before joining date.
        """

        if (
            last_working_date
            and last_working_date < joining_date
        ):
            raise ValidationError(
                "Last working date cannot be earlier than joining date."
            )

    def _validate_manager(
        self,
        employee: Employee,
    ):
        """
        Employee cannot report to themselves.
        """

        if (
            employee.manager
            and employee.manager.pk == employee.pk
        ):
            raise ValidationError(
                "An employee cannot be their own manager."
            )