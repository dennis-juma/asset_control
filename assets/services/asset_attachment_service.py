from django.core.exceptions import ValidationError
from django.db import transaction

from assets.choices.history_choices import AssetHistoryEvent
from assets.dtos.asset_attachment import (
    AssetAttachmentCreateDTO,
    AssetAttachmentUpdateDTO,
)
from assets.models import AssetAttachment
from assets.repositories.asset_attachment_repository import (
    AssetAttachmentRepository,
)
from assets.services.asset_history_service import AssetHistoryService


class AssetAttachmentService:

    def __init__(self):
        self.repository = AssetAttachmentRepository()

    # =====================================================
    # Create
    # =====================================================

    @transaction.atomic
    def create(
        self,
        dto: AssetAttachmentCreateDTO,
        performed_by=None,
    ) -> AssetAttachment:

        self._validate_attachment_type(
            dto,
        )

        attachment = AssetAttachment(
            asset=dto.asset,
            attachment_type=dto.attachment_type,
            file=dto.file,
            description=dto.description or "",
        )

        attachment = self.repository.create(
            attachment,
        )

        AssetHistoryService.log_event(
            asset=dto.asset,
            event_type=AssetHistoryEvent.ATTACHMENT_ADDED,
            performed_by=performed_by,
            reference=str(attachment.pk),
            notes=(
                f"{attachment.get_attachment_type_display()} "
                "attachment added."
            ),
            metadata={
                "attachment_id": str(attachment.pk),
                "attachment_type": attachment.attachment_type,
                "filename": attachment.original_filename,
            },
        )

        return attachment

    # =====================================================
    # Update
    # =====================================================

    @transaction.atomic
    def update(
        self,
        attachment: AssetAttachment,
        dto: AssetAttachmentUpdateDTO,
        performed_by=None,
    ) -> AssetAttachment:

        old_type = attachment.attachment_type
        old_description = attachment.description

        attachment.attachment_type = (
            dto.attachment_type
        )
        attachment.description = (
            dto.description or ""
        )

        attachment = self.repository.update(
            attachment,
        )

        AssetHistoryService.log_event(
            asset=attachment.asset,
            event_type=AssetHistoryEvent.ATTACHMENT_UPDATED,
            performed_by=performed_by,
            reference=str(attachment.pk),
            notes="Asset attachment updated.",
            metadata={
                "attachment_id": str(attachment.pk),
                "old_attachment_type": old_type,
                "new_attachment_type": attachment.attachment_type,
                "old_description": old_description,
                "new_description": attachment.description,
                "filename": attachment.original_filename,
            },
        )

        return attachment

    # =====================================================
    # Delete
    # =====================================================

    @transaction.atomic
    def delete(
        self,
        attachment: AssetAttachment,
        performed_by=None,
    ) -> None:

        asset = attachment.asset
        attachment_id = attachment.pk
        attachment_type = attachment.attachment_type
        filename = attachment.original_filename

        AssetHistoryService.log_event(
            asset=asset,
            event_type=AssetHistoryEvent.ATTACHMENT_DELETED,
            performed_by=performed_by,
            reference=str(attachment_id),
            notes="Asset attachment deleted.",
            metadata={
                "attachment_id": str(attachment_id),
                "attachment_type": attachment_type,
                "filename": filename,
            },
        )

        self.repository.delete(
            attachment,
        )

        # Django does not automatically remove FileField data when a record is
        # deleted. Wait until the transaction commits before touching storage.
        transaction.on_commit(
            lambda: attachment.file.storage.delete(attachment.file.name)
        )

    # =====================================================
    # Validation
    # =====================================================

    def _validate_attachment_type(
        self,
        dto: AssetAttachmentCreateDTO,
    ) -> None:

        if not dto.file:
            raise ValidationError(
                {
                    "file":
                    "Please select an attachment file."
                }
            )
