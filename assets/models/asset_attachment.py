import os

from django.db import models

from assets.choices import AttachmentType
from core.models import BaseModel
from assets.utils.file_validator import (
    validate_attachment_file,
)
from .asset import Asset


def asset_attachment_upload_path(instance, filename):
    extension = os.path.splitext(filename)[1].lower()
    filename = (
    f"{instance.attachment_type.lower()}"
    f"{extension}"
    )

    return f"asset_attachments/{instance.asset.asset_tag}/{filename}"


class AssetAttachment(BaseModel):

    slug_source = "original_filename"

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="attachments",
    )

    attachment_type = models.CharField(
        max_length=20,
        choices=AttachmentType.choices,
    )

    file = models.FileField(
       
        upload_to=asset_attachment_upload_path,
        validators=[validate_attachment_file],
    )

    original_filename = models.CharField(
        max_length=255,
        editable=False,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Asset Attachment"
        verbose_name_plural = "Asset Attachments"
        constraints = [
            models.UniqueConstraint(
                fields=["asset", "attachment_type"],
                name="unique_attachment_type_per_asset",
            )
        ]

    def __str__(self):
        return f"{self.asset.asset_tag} - {self.get_attachment_type_display()}"

    def save(self, *args, **kwargs):
        if self.file:
            self.original_filename = os.path.basename(self.file.name)

        self.full_clean()
        super().save(*args, **kwargs)