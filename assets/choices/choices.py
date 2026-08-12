from django.db import models


class AssetStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE", "Available"
    ASSIGNED = "ASSIGNED", "Assigned"
    RESERVED = "RESERVED", "Reserved"
    IN_TRANSIT = "IN_TRANSIT", "In Transit"

    MAINTENANCE = "MAINTENANCE", "Under Preventive Maintenance"
    UNDER_REPAIR = "UNDER_REPAIR", "Under Repair"

    STOLEN = "STOLEN", "Stolen"
    LOST = "LOST", "Lost"
    RETIRED = "RETIRED", "Retired"
    DISPOSED = "DISPOSED", "Disposed"


class AssetCondition(models.TextChoices):
    NEW = "NEW", "New"
    EXCELLENT = "EXCELLENT", "Excellent"
    GOOD = "GOOD", "Good"
    FAIR = "FAIR", "Fair"
    POOR = "POOR", "Poor"
    DAMAGED = "DAMAGED", "Damaged"

class AssignmentStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    RETURNED = "RETURNED", "Returned"
    TRANSFERRED = "TRANSFERRED", "Transferred"

class AssignmentType(models.TextChoices):
    EMPLOYEE = "EMPLOYEE", "Employee"
    SITE = "SITE", "Site"
