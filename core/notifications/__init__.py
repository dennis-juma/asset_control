    

__all__ = [
    "NotificationEvent",
    "Notification",
    "NotificationService",
]


def __getattr__(name):

    if name == "NotificationEvent":
        from .enums import NotificationEvent
        return NotificationEvent

    if name == "Notification":
        from .models import Notification
        return Notification

    if name == "NotificationService":
        from .service import NotificationService
        return NotificationService

    raise AttributeError(
        f"module {__name__!r} has no attribute {name!r}"
    )