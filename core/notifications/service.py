from django.contrib import messages

from core.dtos.notification import NotificationDTO


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