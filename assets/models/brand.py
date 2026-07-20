from django.core.exceptions import ValidationError
from django.db import models

from core.models import BaseModel
from core.utils.code import generate_code
from organizations.models import Company


class Brand(BaseModel):
    """
    Asset manufacturer.

    Examples:
        - Dell
        - HP
        - Lenovo
        - Cisco
    """

    slug_source = "name"

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="brands",
    )

    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=10,
        blank=True,
        editable=False,
    )

    website = models.URLField(
        blank=True,
    )

    support_email = models.EmailField(
        blank=True,
    )

    support_phone = models.CharField(
        max_length=30,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

        constraints = [
            models.UniqueConstraint(
                fields=["company", "name"],
                name="unique_brand_name_per_company",
            ),
            models.UniqueConstraint(
                fields=["company", "code"],
                name="unique_brand_code_per_company",
            ),
        ]

    def clean(self):
        super().clean()

        self.name = self.name.strip()

        if not self.name:
            raise ValidationError({
                "name": "Brand name cannot be empty."
            })

        if Brand.objects.filter(
            company=self.company,
            name__iexact=self.name,
        ).exclude(pk=self.pk).exists():
            raise ValidationError({
                "name": "A brand with this name already exists for this company."
            })

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name