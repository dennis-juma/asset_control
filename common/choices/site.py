from django.db import models


class SiteType(models.TextChoices):
    HEAD_OFFICE = "HQ", "Head Office"
    REGIONAL_OFFICE = "RO", "Regional Office"
    WAREHOUSE = "WH", "Warehouse"
    CALL_CENTER = "CC", "Call Center"
    FIELD_BASE = "FB", "Field Base"
    SERVICE_CENTER = "SC", "Service Center"
    RETAIL_SHOP = "AHQ", "Area Head Quater"
    TRAINING_CENTER = "TC", "Training Center"