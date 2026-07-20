from django.db import models


class AssetType(models.TextChoices):
    PHYSICAL = "PHYSICAL", "Physical"
    DIGITAL = "DIGITAL", "Digital"