from django.db import models


class AssetHistoryEvent(models.TextChoices):
    CREATED = "CREATED", "Created"
    UPDATED = "UPDATED", "Updated"

    ASSIGNED = "ASSIGNED", "Assigned"
    RETURNED = "RETURNED", "Returned"
    TRANSFERRED = "TRANSFERRED", "Transferred"

    STATUS_CHANGED = "STATUS_CHANGED", "Status Changed"

    MAINTENANCE_STARTED = "MAINTENANCE_STARTED", "Maintenance Started"
    MAINTENANCE_COMPLETED = "MAINTENANCE_COMPLETED", "Maintenance Completed"
    MAINTENANCE_CANCELLED = "MAINTENANCE_CANCELLED", "Maintenance Cancelled"

    WARRANTY_ADDED = "WARRANTY_ADDED", "Warranty Added"
    WARRANTY_UPDATED = "WARRANTY_UPDATED", "Warranty Updated"