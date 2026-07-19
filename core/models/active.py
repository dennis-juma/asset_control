from django.db import models
from django.utils import timezone


class IsActiveModel(models.Model):


    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    activated_at = models.DateTimeField(
        auto_now_add=True,
    )

    deactivated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def deactivate(self):
        self.is_active = False
        self.deactivated_at = timezone.now()
        self.save(update_fields=["is_active", "deactivated_at"])

    def activate(self):
        self.is_active = True
        self.deactivated_at = None
        self.save(update_fields=["is_active", "deactivated_at"])