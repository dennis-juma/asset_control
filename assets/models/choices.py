from django.db import models


class AssetType(models.TextChoices):
    PHYSICAL = "PHYSICAL", "Physical"
    DIGITAL = "DIGITAL", "Digital"


class VendorType(models.TextChoices):
    SUPPLIER = "SUPPLIER", "Supplier"
    RESELLER = "RESELLER", "Reseller"
    MANUFACTURER = "MANUFACTURER", "Manufacturer"
    SERVICE_PROVIDER = "SERVICE_PROVIDER", "Service Provider"

class AssetStatus(models.TextChoices):
    IN_STOCK = "IN_STOCK", "In Stock"
    ASSIGNED = "ASSIGNED", "Assigned"
    RESERVED = "RESERVED", "Reserved"
    IN_TRANSIT = "IN_TRANSIT", "In Transit"
    UNDER_REPAIR = "UNDER_REPAIR", "Under Repair"
    RETIRED = "RETIRED", "Retired"
    LOST = "LOST", "Lost"
    STOLEN = "STOLEN", "Stolen"
    DISPOSED = "DISPOSED", "Disposed"


class AssetCondition(models.TextChoices):
    NEW = "NEW", "New"
    EXCELLENT = "EXCELLENT", "Excellent"
    GOOD = "GOOD", "Good"
    FAIR = "FAIR", "Fair"
    POOR = "POOR", "Poor"
    DAMAGED = "DAMAGED", "Damaged"