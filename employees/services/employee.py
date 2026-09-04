from django.core.exceptions import ValidationError
from django.db import transaction
from accounts.models.choices import UserType
from accounts.models import User, UserCountryAccess
from accounts.services.user_provisioning import (
    UserProvisioningService,
)
from assets.services.asset_notification_service import (
    AssetNotificationService,
)

from core.notifications.service import NotificationService
from core.notifications.enums import NotificationEvent


from employees.dtos import (
    EmployeeCreateDTO,
    EmployeeUpdateDTO,
)
from employees.models import Employee
from employees.repositories import EmployeeRepository


class EmployeeService:

    def __init__(self):
        self.repository = EmployeeRepository()
    @transaction.atomic
    def create_employee(
        self,
        dto: EmployeeCreateDTO,
    ) -> Employee:

        self._validate_dates(
            dto.joining_date,
            dto.last_working_date,
        )

        employee = Employee(
            country=dto.country,
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
            remarks=dto.remarks,
        )

        employee.full_clean()

        employee = self.repository.create(employee)

        UserProvisioningService.provision_for_employee(
            employee
        )

        return employee

    @transaction.atomic
    def update_employee(
        self,
        employee: Employee,
        dto: EmployeeUpdateDTO,
    ) -> Employee:

        self._validate_dates(
            dto.joining_date,
            dto.last_working_date,
        )

        # Detect deactivation BEFORE changing the employee
        is_being_deactivated = (
            employee.is_active
            and not dto.is_active
        )

        employee.country = dto.country
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
        employee.remarks = dto.remarks
        employee.is_active = dto.is_active

        self._validate_manager(employee)

        employee.full_clean()

        employee = self.repository.update(employee)

        UserProvisioningService.sync_for_employee(
            employee,
            user_type=dto.system_role,
        )

    # -------------------------------------------------
    # Employee Offboarding Notification
    # -------------------------------------------------

        if is_being_deactivated:

            assigned_assets = (
                AssetNotificationService.employee_assets(
                    employee
                )
            )

            if employee.user and employee.user.email:

                NotificationService.send_email(
                    event=NotificationEvent.EMPLOYEE_OFFBOARDING,
                    recipient=employee.user,
                    subject="Employee Offboarding - Asset Return Required",
                    template="emails/employee_offboarding.html",
                    context={
                        "employee": employee,
                        "assigned_assets": assigned_assets,
                        "asset_count": assigned_assets.count(),
                    },
                )

        return employee
        

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

    def _validate_user(
    self,
    user,
):
        """
        A user can only be linked to one Employee record.
        """

        if user is None:
            return

        if Employee.objects.filter(
            user=user,
        ).exists():

            raise ValidationError(
                {
                    "user": [
                        "This user is already linked to an employee."
                    ]
                }
            )