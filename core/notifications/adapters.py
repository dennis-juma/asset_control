from django.contrib.messages import get_messages

from core.dtos.notification import NotificationDTO
from .enums import NotificationLevel


class DjangoMessagesAdapter:

    @staticmethod
    def to_dtos(request):

        notifications = []

        level_map = {
            "success": NotificationLevel.SUCCESS,
            "info": NotificationLevel.INFO,
            "warning": NotificationLevel.WARNING,
            "error": NotificationLevel.ERROR,
        }

        for message in get_messages(request):

            notifications.append(
                NotificationDTO.create(
                    title=message.tags.title(),
                    message=str(message),
                    level=level_map.get(
                        message.tags,
                        NotificationLevel.INFO,
                    ),
                )
            )

        return notifications