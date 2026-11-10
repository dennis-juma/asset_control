import io
import tempfile
from datetime import date
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from openpyxl import load_workbook

from document_processing.models import ExtractionBatch, ExtractionDocument, ExtractedEquipmentRecord
from document_processing.models import private_document_storage
from document_processing.services.extraction import parse_extraction_response, process_document
from document_processing.services.export import export_records
from organizations.models import Country, Site


@override_settings(MEDIA_ROOT="/tmp/ams-media", PRIVATE_MEDIA_ROOT="/tmp/ams-private", GEMINI_API_KEY="test")
class DocumentProcessingTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.storage_tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        private_document_storage.__dict__["location"] = cls.storage_tmp.name

    @classmethod
    def tearDownClass(cls):
        cls.storage_tmp.cleanup()
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_superuser(username="docadmin", email="doc@example.com", password="not-a-real-secret")
        cls.country = Country.objects.create(name="Testland", iso2="TL", iso3="TST", phone_code="+1")

    def test_parse_preserves_leading_zero_and_normalizes_date(self):
        rows = parse_extraction_response({"employee_name": "A Person", "records": [{"equipment_type": "Laptop/PC", "serial_number": "0000123", "date_received": "04/03/2025"}]})
        self.assertEqual(rows[0]["serial_number"], "0000123")
        self.assertEqual(rows[0]["date_received"], date(2025, 3, 4))
        self.assertEqual(rows[0]["raw_extraction_data"]["record"]["date_received"], "04/03/2025")

    def test_upload_creates_queued_batch_and_rejects_invalid_pdf(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("document_processing:upload"), {"name": "Batch", "country": str(self.country.pk), "files": SimpleUploadedFile("checklist.pdf", b"%PDF-1.4\n%%EOF", content_type="application/pdf")})
        self.assertEqual(response.status_code, 302, getattr(response, "context", None)["form"].errors if response.context and response.context.get("form") else response.content[:1000])
        doc = ExtractionDocument.objects.get()
        self.assertEqual(doc.processing_status, ExtractionDocument.Status.QUEUED)
        detail = self.client.get(reverse("document_processing:batch-detail", args=[doc.batch_id]))
        self.assertEqual(detail.status_code, 200)
        invalid = self.client.post(reverse("document_processing:upload"), {"files": SimpleUploadedFile("bad.pdf", b"not pdf", content_type="application/pdf")})
        self.assertEqual(invalid.status_code, 200)
        self.assertEqual(ExtractionBatch.objects.count(), 1)

    def test_processing_creates_records_once_and_is_idempotent(self):
        batch = ExtractionBatch.objects.create(uploaded_by=self.user, country=self.country)
        upload = SimpleUploadedFile("scan.pdf", b"%PDF-1.4\n%%EOF", content_type="application/pdf")
        document = ExtractionDocument(batch=batch, original_filename="scan.pdf", file_size=upload.size, sha256="a" * 64)
        document.stored_file.save("scan.pdf", upload, save=True)
        response = {"records": [{"employee_name": "A Person", "equipment_type": "Mobile Phone", "serial_number": "00102"}]}
        with patch("document_processing.services.extraction.PdfReader") as reader, patch("document_processing.services.extraction.record_audit", create=True):
            reader.return_value.pages = [object()]
            process_document(document.pk, response_factory=lambda *_: response)
            process_document(document.pk, response_factory=lambda *_: self.fail("completed documents must not be reprocessed"))
        self.assertEqual(document.records.count(), 1)
        self.assertEqual(document.records.get().serial_number, "00102")

    def test_failed_document_can_be_retried_without_duplicate_records(self):
        batch = ExtractionBatch.objects.create(uploaded_by=self.user, country=self.country)
        upload = SimpleUploadedFile("retry.pdf", b"%PDF-1.4\n%%EOF", content_type="application/pdf")
        document = ExtractionDocument(batch=batch, original_filename="retry.pdf", file_size=upload.size, sha256="d" * 64)
        document.stored_file.save("retry.pdf", upload, save=True)
        with patch("document_processing.services.extraction.PdfReader") as reader:
            reader.return_value.pages = [object()]
            process_document(document.pk, response_factory=lambda *_: {"records": "not a list"})
            document.refresh_from_db()
            self.assertEqual(document.processing_status, ExtractionDocument.Status.FAILED)
            document.processing_status = ExtractionDocument.Status.QUEUED
            document.save(update_fields=["processing_status"])
            process_document(document.pk, response_factory=lambda *_: {"records": [{"employee_name": "Retry Person", "serial_number": "0009"}]})
        self.assertEqual(document.records.count(), 1)
        self.assertEqual(document.records.get().serial_number, "0009")

    def test_review_edit_history_and_excel_export(self):
        batch = ExtractionBatch.objects.create(uploaded_by=self.user, country=self.country)
        upload = SimpleUploadedFile("scan.pdf", b"%PDF-1.4\n%%EOF", content_type="application/pdf")
        document = ExtractionDocument(batch=batch, original_filename="scan.pdf", file_size=upload.size, sha256="b" * 64)
        document.stored_file.save("scan.pdf", upload, save=True)
        record = ExtractedEquipmentRecord.objects.create(batch=batch, document=document, employee_name="Before", serial_number="000012", raw_extraction_data={"serial_number": "000012"})
        self.client.force_login(self.user)
        response = self.client.post(reverse("document_processing:record-review", args=[record.pk]), {"employee_name": "After", "equipment_type": "Laptop/PC", "make": "A", "model": "B", "serial_number": "000012", "date_received": "04/03/2025", "issued_by": "Issuer", "comments": "Replacement", "review_comments": "checked", "action": "review"})
        self.assertEqual(response.status_code, 302)
        record.refresh_from_db()
        self.assertEqual(record.employee_name, "After")
        self.assertEqual(record.serial_number, "000012")
        self.assertEqual(record.review_status, ExtractedEquipmentRecord.ReviewStatus.REVIEWED)
        self.assertTrue(record.flagged_for_review is False)
        self.assertEqual(record.edit_history.count(), 1, {"response": response.status_code, "name": record.employee_name, "review": record.review_status, "history": list(record.edit_history.values())})
        response = export_records(ExtractedEquipmentRecord.objects.filter(pk=record.pk))
        workbook = load_workbook(io.BytesIO(response.content))
        self.assertEqual(workbook["Extracted Records"]["G2"].value, "000012")
        self.assertEqual(workbook["Extracted Records"]["H2"].value, "04/03/2025")
        self.assertIn("Instructions", workbook.sheetnames)

    def test_unauthorized_user_cannot_open_private_document(self):
        batch = ExtractionBatch.objects.create(uploaded_by=self.user, country=self.country)
        upload = SimpleUploadedFile("scan.pdf", b"%PDF-1.4\n%%EOF", content_type="application/pdf")
        document = ExtractionDocument(batch=batch, original_filename="scan.pdf", file_size=upload.size, sha256="c" * 64)
        document.stored_file.save("scan.pdf", upload, save=True)
        User = get_user_model()
        user = User.objects.create_user(username="limited", email="limited@example.com", password="pass12345")
        self.client.force_login(user)
        response = self.client.get(reverse("document_processing:document", args=[document.pk]))
        self.assertIn(response.status_code, (302, 403))
        response.close()

