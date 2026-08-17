from enum import Enum
from django.db import models



class NotificationLevel(str, Enum):
    SUCCESS = "success"
    INFO = "info"
    WARNING = "warning"
    ERROR = "danger"


class NotificationStyle(str, Enum):
    ALERT = "alert"
    TOAST = "toast"



class NotificationEvent(models.TextChoices):

    ASSET_ASSIGNED = (
        "ASSET_ASSIGNED",
        "Asset Assigned",
    )

    ASSET_TRANSFERRED = (
        "ASSET_TRANSFERRED",
        "Asset Transferred",
    )

    ASSET_RETURNED = (
        "ASSET_RETURNED",
        "Asset Returned",
    )

    EMPLOYEE_OFFBOARDING = (
        "EMPLOYEE_OFFBOARDING",
        "Employee Offboarding",
    )

    ASSET_LIFECYCLE = (
        "ASSET_LIFECYCLE",
        "Asset Lifecycle",
    )

    IMPORT_COMPLETED = (
        "IMPORT_COMPLETED",
        "Import Completed",
    )

    IMPORT_FAILED = (
        "IMPORT_FAILED",
        "Import Failed",
    )

    SYSTEM = (
        "SYSTEM",
        "System",
    )