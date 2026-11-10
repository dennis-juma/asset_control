import hashlib
import os
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models


def private_document_path(instance, filename):
    extension = os.path.splitext(filename)[1].lower() or ".pdf"
    return f"asset_document_processing/{instance.batch_id}/{instance.id}{extension}"


from document_processing.storage import PrivateDocumentStorage

private_document_storage = PrivateDocumentStorage()


def validate_pdf(file):
    if file.size > settings.EXTRACTION_MAX_FILE_SIZE:
        raise ValidationError("PDF files must be 20 MB or smaller.")
    if file.read(5) != b"%PDF-":
        raise ValidationError("The uploaded file is not a valid PDF.")
    file.seek(0)


class ExtractionBatch(models.Model):
    class Status(models.TextChoices):
        UPLOADED = "UPLOADED", "Uploaded"
        PROCESSING = "PROCESSING", "Processing"
        COMPLETED = "COMPLETED", "Completed"
        PARTIAL = "PARTIAL", "Partially failed"
        FAILED = "FAILED", "Failed"
        REVIEW = "REVIEW", "Review"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch_number = models.CharField(max_length=30, unique=True, editable=False)
    name = models.CharField(max_length=200, blank=True)
    country = models.ForeignKey("organizations.Country", null=True, blank=True, on_delete=models.PROTECT, related_name="extraction_batches")
    site = models.ForeignKey("organizations.Site", null=True, blank=True, on_delete=models.PROTECT, related_name="extraction_batches")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="extraction_batches")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPLOADED, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-uploaded_at"]
        permissions = [("process_documents", "Can upload and process checklist documents"), ("review_extracted_records", "Can review extracted records"), ("export_extracted_records", "Can export extracted records")]

    def save(self, *args, **kwargs):
        if not self.batch_number:
            self.batch_number = f"EDP-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    @property
    def total_files(self):
        return self.documents.count()

    @property
    def processed_files(self):
        return self.documents.filter(processing_status=ExtractionDocument.Status.COMPLETED).count()

    @property
    def failed_files(self):
        return self.documents.filter(processing_status=ExtractionDocument.Status.FAILED).count()

    @property
    def total_records(self):
        return self.records.count()

    def __str__(self):
        return self.batch_number


class ExtractionDocument(models.Model):
    class Status(models.TextChoices):
        QUEUED = "QUEUED", "Queued"
        PROCESSING = "PROCESSING", "Processing"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch = models.ForeignKey(ExtractionBatch, on_delete=models.CASCADE, related_name="documents")
    original_filename = models.CharField(max_length=255)
    stored_file = models.FileField(upload_to=private_document_path, storage=private_document_storage, validators=[FileExtensionValidator(["pdf"]), validate_pdf])
    file_size = models.PositiveBigIntegerField(default=0)
    sha256 = models.CharField(max_length=64, db_index=True)
    page_count = models.PositiveIntegerField(null=True, blank=True)
    processing_status = models.CharField(max_length=20, choices=Status.choices, default=Status.QUEUED, db_index=True)
    processing_attempts = models.PositiveSmallIntegerField(default=0)
    processing_started_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["uploaded_at"]
        constraints = [models.UniqueConstraint(fields=["batch", "sha256"], name="unique_extraction_file_per_batch")]

    def __str__(self):
        return self.original_filename


class ExtractedEquipmentRecord(models.Model):
    class ReviewStatus(models.TextChoices):
        PENDING = "PENDING", "Pending review"
        REVIEWED = "REVIEWED", "Reviewed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch = models.ForeignKey(ExtractionBatch, on_delete=models.CASCADE, related_name="records")
    document = models.ForeignKey(ExtractionDocument, on_delete=models.CASCADE, related_name="records")
    record_index = models.PositiveIntegerField(default=0)
    employee_name = models.CharField(max_length=255, blank=True)
    equipment_type = models.CharField(max_length=100, blank=True)
    make = models.CharField(max_length=150, blank=True)
    model = models.CharField(max_length=150, blank=True)
    serial_number = models.CharField(max_length=150, blank=True)
    date_received = models.DateField(null=True, blank=True)
    issued_by = models.CharField(max_length=255, blank=True)
    comments = models.TextField(blank=True)
    review_comments = models.TextField(blank=True)
    validation_warnings = models.JSONField(default=list, blank=True)
    flagged_for_review = models.BooleanField(default=False, db_index=True)
    page_number = models.PositiveIntegerField(null=True, blank=True)
    raw_extraction_data = models.JSONField(default=dict)
    confidence_score = models.FloatField(null=True, blank=True)
    review_status = models.CharField(max_length=20, choices=ReviewStatus.choices, default=ReviewStatus.PENDING, db_index=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="reviewed_extraction_records")
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["document__uploaded_at", "record_index"]
        constraints = [models.UniqueConstraint(fields=["document", "record_index"], name="unique_extracted_record_per_document")]
        indexes = [models.Index(fields=["batch", "review_status"]), models.Index(fields=["serial_number"])]

    def __str__(self):
        return f"{self.employee_name} — {self.equipment_type} ({self.document.original_filename})"


class ExtractionRecordEdit(models.Model):
    record = models.ForeignKey(ExtractedEquipmentRecord, on_delete=models.CASCADE, related_name="edit_history")
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    before = models.JSONField(default=dict)
    after = models.JSONField(default=dict)
    edited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-edited_at"]

