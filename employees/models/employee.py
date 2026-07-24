from django.db import models

from core.models import BaseModel
from core.services import CodeGenerator
from core.utils.slug import generate_unique_slug

from organizations.models import (
    Company,
    Department,
    JobTitle,
    Site,
)


class EmploymentStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    TERMINATED = "TERMINATED", "Terminated"
    RESIGNED = "RESIGNED", "Resigned"
    SUSPENDED = "SUSPENDED", "Suspended"


class Gender(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female",



class Employee(BaseModel):

    slug_source = "first_name"
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="employees",
    )

    employee_number = models.CharField(
        max_length=15,
        unique=True,
        editable=False,
        blank=True,
    )

    first_name = models.CharField(max_length=100)

    middle_name = models.CharField(
        max_length=100,
        blank=True,
    )

    last_name = models.CharField(max_length=100)

    email = models.EmailField(
        unique=True,
        blank=True,
    )

    phone_number = models.CharField(
        max_length=30,
        blank=True,
    )

    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        blank=True,
    )


    hire_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.ACTIVE,
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="employees",
    )

    job_title = models.ForeignKey(
        JobTitle,
        on_delete=models.PROTECT,
        related_name="employees",
    )

    site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        related_name="employees",
    )

    manager = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="subordinates",
    )

    profile_photo = models.ImageField(
        upload_to="employees/photos/",
        blank=True,
        null=True,
    )

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["employee_number"]

    def __str__(self):
        return f"{self.employee_number} - {self.first_name} {self.last_name}"


    def save(self, *args, **kwargs):
        if not self.employee_number:
            self.employee_number = CodeGenerator.generate(
                model=Employee,
                field="employee_number",
                prefix="EMP",
                digits=6,
            )
        if not self.slug:
            self.slug = generate_unique_slug( 
                self,
            f"{self.first_name} {self.last_name}")

           

        super().save(*args, **kwargs)