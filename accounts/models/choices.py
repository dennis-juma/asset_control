from django.db import models


class UserType(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    ADMIN = "ADMIN", "Administrator"
    COUNTRY_ADMIN = "COUNTRY_ADMIN", "Country Admin"
    USER = "USER", "User"