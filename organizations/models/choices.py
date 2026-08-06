from django.db import models


class LocationType(models.TextChoices):
    OFFICE = "Head Office", "Head Office"
    CALL_CENTER = "Call Center", "Call Center"
    WAREHOUSE = "Warehouse", "Warehouse"
    SERVICE_CENTER = "Service Center", "Service Center"
    SHOP = "Area HQ", "Area HQ"

class Status(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"


class Gender(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
