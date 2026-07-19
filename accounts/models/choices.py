from django.db import models


class UserType(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    ADMIN = "ADMIN", "Administrator"
    IT_MANAGER = "IT_MANAGER", "IT Manager"
    STORE_MANAGER = "STORE_MANAGER", "Store Manager"
    AUDITOR = "AUDITOR", "Auditor"
    EMPLOYEE = "EMPLOYEE", "Employee"