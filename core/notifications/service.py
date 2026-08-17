from django.contrib import messages

from core.dtos.notification import NotificationDTO
from django.utils import timezone

from .email import NotificationEmailService
from .models import Notification

class NotificationService:

    LEVEL_MAPPING = {
        "success": messages.SUCCESS,
        "info": messages.INFO,
        "warning": messages.WARNING,
        "danger": messages.ERROR,
    }

    @classmethod
    def send(
        cls,
        request,
        notification: NotificationDTO,
    ):

        messages.add_message(
            request,
            cls.LEVEL_MAPPING[
                notification.level.value
            ],
            notification.message,
        )


    @classmethod
    def send_email(
        cls,
        *,
        event,
        recipient,
        subject,
        template,
        context=None,
    ):

        if not recipient:
            return None

        email = getattr(
            recipient,
            "email",
            "",
        )

        if not email:
            return None

        notification = Notification.objects.create(
            event=event,
            recipient=recipient,
            recipient_email=email,
            subject=subject,
        )

        try:

            NotificationEmailService.send(
                recipient_email=email,
                subject=subject,
                template=template,
                context=context,
            )

            notification.is_sent = True
            notification.sent_at = timezone.now()

            notification.save(
                update_fields=[
                    "is_sent",
                    "sent_at",
                ]
            )

        except Exception as exc:

            notification.error_message = str(exc)

            notification.save(
                update_fields=[
                    "error_message",
                ]
            )

            raise

        return notification