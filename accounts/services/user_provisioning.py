from django.db import transaction

from accounts.models import User, UserCountryAccess
from accounts.models.choices import UserType


class UserProvisioningService:

    @staticmethod
    @transaction.atomic
    def provision_for_employee(employee):

        if employee.user_id:
            return employee.user

        username = employee.employee_id

        user = User.objects.create_user(
            username=username,
            first_name=employee.first_name,
            last_name=employee.last_name,
            email=employee.email,
            employee_id=employee.employee_id,
            phone=employee.phone,
            user_type=UserType.USER,
            is_active=employee.is_current_employee,
        )

        user.set_unusable_password()
        user.save(
            update_fields=["password"]
        )

        employee.user = user
        employee.save(
            update_fields=["user"]
        )

        if employee.country_id:
            UserCountryAccess.objects.get_or_create(
                user=user,
                country_id=employee.country_id,
            )

        return user


    
    @staticmethod
    @transaction.atomic
    def sync_for_employee(employee):
        """
        Synchronize an employee's system account.

        Updates:
        - name
        - email
        - phone
        - employee ID / username
        - active status
        - country access
        """

        if not employee.user_id:
            return UserProvisioningService.provision_for_employee(
                employee
            )

        user = employee.user

        user.username = employee.employee_id
        user.employee_id = employee.employee_id
        user.first_name = employee.first_name
        user.last_name = employee.last_name
        user.email = employee.email
        user.phone = employee.phone
        user.is_active = employee.is_current_employee

        user.save(
            update_fields=[
                "username",
                "employee_id",
                "first_name",
                "last_name",
                "email",
                "phone",
                "is_active",
            ]
        )

        # Synchronize country access.
        UserCountryAccess.objects.filter(
            user=user,
        ).exclude(
            country_id=employee.country_id,
        ).delete()

        if employee.country_id:
            UserCountryAccess.objects.get_or_create(
                user=user,
                country_id=employee.country_id,
            )

        return user