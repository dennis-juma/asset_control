from django.db import models


class UserRole(models.TextChoices):

    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"

    ADMIN = "ADMIN", "Administrator"

    USER = "USER", "User"