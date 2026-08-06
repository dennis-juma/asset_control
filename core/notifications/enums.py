from enum import Enum


class NotificationLevel(str, Enum):
    SUCCESS = "success"
    INFO = "info"
    WARNING = "warning"
    ERROR = "danger"


class NotificationStyle(str, Enum):
    ALERT = "alert"
    TOAST = "toast"