from django.db import models

from core.models import BaseModel


class Asset(BaseModel):
    """
    Represents a physical company asset.
    Additional fields will be added incrementally.
    """

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"

    def __str__(self):
        return str(self.id)