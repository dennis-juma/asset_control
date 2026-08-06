from dataclasses import dataclass
from uuid import uuid4

from core.notifications.enums import (
    NotificationLevel,
    NotificationStyle,
)


@dataclass(slots=True, frozen=True)
class NotificationDTO:

    id: str

    title: str

    message: str

    level: NotificationLevel

    style: NotificationStyle = NotificationStyle.ALERT

    icon: str | None = None

    dismissible: bool = True

    auto_close: bool = True

    timeout: int = 5000

    html: bool = False

    @classmethod
    def create(
        cls,
        title: str,
        message: str,
        level: NotificationLevel,
        **kwargs,
    ):
        return cls(
            id=f"notification-{uuid4().hex}",
            title=title,
            message=message,
            level=level,
            **kwargs,
        )