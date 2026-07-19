from django.contrib.auth.models import AbstractUser
from django.db import models

from .choices import UserType


class User(AbstractUser):
    """
    Custom User Model
    """

    employee_id = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        unique=True,
        help_text="Employee ID from HR system",
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    profile_photo = models.ImageField(
        upload_to="users/profile/",
        blank=True,
        null=True,
    )

    user_type = models.CharField(
        max_length=30,
        choices=UserType.choices,
        default=UserType.EMPLOYEE,
    )

    def __str__(self):
        return self.get_full_name() or self.username