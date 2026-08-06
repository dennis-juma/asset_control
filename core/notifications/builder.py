from core.dtos.notification import NotificationDTO

from .enums import (
    NotificationLevel,
    NotificationStyle,
)


class NotificationBuilder:

    def success(self, title, message, **kwargs):

        return NotificationDTO.create(
            title,
            message,
            NotificationLevel.SUCCESS,
            **kwargs,
        )

    def info(self, title, message, **kwargs):

        return NotificationDTO.create(
            title,
            message,
            NotificationLevel.INFO,
            **kwargs,
        )

    def warning(self, title, message, **kwargs):

        return NotificationDTO.create(
            title,
            message,
            NotificationLevel.WARNING,
            **kwargs,
        )

    def error(self, title, message, **kwargs):

        return NotificationDTO.create(
            title,
            message,
            NotificationLevel.ERROR,
            **kwargs,
        )

    def toast(self, notification: NotificationDTO):

        return NotificationDTO(
            **{
                **notification.__dict__,
                "style": NotificationStyle.TOAST,
            }
        )