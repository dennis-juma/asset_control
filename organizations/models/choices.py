from django.db import models


class LocationType(models.TextChoices):
    OFFICE = "OFFICE", "Head Office"
    CALL_CENTER = "CALL_CENTER", "Call Center"
    WAREHOUSE = "WAREHOUSE", "Warehouse"
    SERVICE_CENTER = "SERVICE_CENTER", "Service Center"
    SHOP = "AHQ", "AHQ"
