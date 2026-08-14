from django.conf import settings
from django.db import models


class UserCountryAccess(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="country_access",
    )

    country = models.ForeignKey(
        "organizations.Country",
        on_delete=models.CASCADE,
        related_name="user_access",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "country"],
                name="unique_user_country_access",
            ),
        ]

        ordering = ["country__name"]

        verbose_name = "User Country Access"
        verbose_name_plural = "User Country Access"

    def __str__(self):
        return f"{self.user} - {self.country}"