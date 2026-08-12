from django.db import models


class AssetType(models.TextChoices):
    PHYSICAL = "PHYSICAL", "Physical"
    DIGITAL = "DIGITAL", "Digital"


class VendorType(models.TextChoices):
    SUPPLIER = "SUPPLIER", "Supplier"
    RESELLER = "RESELLER", "Reseller"
    MANUFACTURER = "MANUFACTURER", "Manufacturer"
    SERVICE_PROVIDER = "SERVICE_PROVIDER", "Service Provider"
