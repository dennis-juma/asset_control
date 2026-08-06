from django.contrib.messages import get_messages

from core.dtos.notification import NotificationDTO
from .enums import NotificationLevel


class DjangoMessagesAdapter:

    @staticmethod
    def to_dtos(request):

        notifications = []

        for message in get_messages(request):

            notifications.append(
                NotificationDTO.create(
                    title=message.tags.title(),
                    message=str(message),
                    level=NotificationLevel(message.tags),
                )
            )

        return notifications