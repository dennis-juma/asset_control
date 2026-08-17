from django.conf import settings
from django.db import models

from .enums import NotificationEvent


class Notification(models.Model):

    event = models.CharField(
        max_length=50,
        choices=NotificationEvent.choices,
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    recipient_email = models.EmailField()

    subject = models.CharField(
        max_length=255,
    )

    message = models.TextField(
        blank=True,
    )

    is_sent = models.BooleanField(
        default=False,
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    error_message = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = [
            "-created_at",
        ]

        indexes = [
            models.Index(
                fields=[
                    "recipient",
                    "is_sent",
                ]
            ),
            models.Index(
                fields=[
                    "event",
                ]
            ),
            models.Index(
                fields=[
                    "created_at",
                ]
            ),
        ]

    def __str__(self):
        return (
            f"{self.event} → "
            f"{self.recipient_email}"
        )