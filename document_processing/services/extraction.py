import json
from io import BytesIO
import logging
import os
import random
import tempfile
import time
from datetime import datetime

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from pypdf import PdfReader

from document_processing.models import ExtractionBatch, ExtractionDocument, ExtractedEquipmentRecord

logger = logging.getLogger(__name__)
FIELDS = ("employee_name", "equipment_type", "make", "model", "serial_number", "date_received", "issued_by", "comments", "page_number")


class ExtractionError(Exception):
    pass


def parse_extraction_response(response):
    if isinstance(response, dict):
        data = response
    else:
        text = getattr(response, "text", response)
        if not isinstance(text, str):
            raise ExtractionError("The extraction service returned no text.")
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        try:
            data = json.loads(text)
        except (ValueError, TypeError) as exc:
            raise ExtractionError("The extraction service returned invalid JSON.") from exc
    if not isinstance(data, dict) or not isinstance(data.get("records", []), list):
        raise ExtractionError("The extraction response must contain a records list.")
    normalized = []
    employee_name = str(data.get("employee_name") or "").strip()
    for row in data.get("records", []):
        if not isinstance(row, dict):
            continue
        equipment_fields = ("equipment_type", "make", "model", "serial_number", "date_received", "issued_by", "comments")
        if not any(str(row.get(field) or "").strip() for field in equipment_fields):
            continue
        item = {field: row.get(field) for field in FIELDS}
        item["employee_name"] = str(item.get("employee_name") or employee_name).strip()
        item["equipment_type"] = str(item.get("equipment_type") or "").strip()
        if item["equipment_type"] and item["equipment_type"].casefold() not in {"mobile phone", "laptop/pc", "other device / merchandise"}:
            item["equipment_type"] = "Other Device / Merchandise"
        for field in ("make", "model", "serial_number", "issued_by", "comments"):
            item[field] = str(item.get(field) or "").strip()
        item["page_number"] = _positive_int(item.get("page_number"))
        item["confidence_score"] = _confidence(row.get("confidence_score"))
        warnings = row.get("validation_warnings", [])
        item["validation_warnings"] = [str(value) for value in warnings] if isinstance(warnings, list) else []
        raw_date = str(item.get("date_received") or "").strip()
        item["date_received"] = parse_date(raw_date)
        if raw_date and item["date_received"] is None:
            item["validation_warnings"].append("Date Received could not be parsed; review required.")
        if not item["employee_name"]:
            item["validation_warnings"].append("Employee name is unreadable or missing.")
        if item["confidence_score"] is not None and item["confidence_score"] < 0.7:
            item["validation_warnings"].append("Low extraction confidence; verify this record manually.")
        item["raw_extraction_data"] = {"document_employee_name": data.get("employee_name"), "record": dict(row)}
        normalized.append(item)
    if not normalized and employee_name:
        normalized.append({"employee_name": employee_name, "equipment_type": "", "make": "", "model": "", "serial_number": "", "date_received": None, "issued_by": "", "comments": "", "page_number": 1, "confidence_score": None, "validation_warnings": ["No equipment items were found; verify the checklist."], "raw_extraction_data": {"employee_name": employee_name, "records": []}})
    return normalized


def parse_date(value):
    if not value:
        return None
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%d.%m.%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def _positive_int(value):
    try:
        number = int(value)
        return number if number > 0 else None
    except (ValueError, TypeError):
        return None


def _confidence(value):
    try:
        result = float(value)
        return max(0.0, min(1.0, result))
    except (ValueError, TypeError):
        return None


def _gemini_response(pdf_bytes, filename):
    api_key = getattr(settings, "GEMINI_API_KEY", "") or os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        raise ExtractionError("GEMINI_API_KEY is not configured.")
    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        raise ExtractionError("Install the google-genai package to enable Gemini extraction.") from exc
    client = genai.Client(api_key=api_key)
    model = settings.GEMINI_MODEL
    prompt = """Read this scanned employee equipment checklist. Return only JSON shaped as {\"employee_name\": string, \"records\": [{\"employee_name\": string, \"equipment_type\": string, \"make\": string, \"model\": string, \"serial_number\": string, \"date_received\": string, \"issued_by\": string, \"comments\": string, \"page_number\": integer, \"confidence_score\": number, \"validation_warnings\": [string]}]}. Extract one record per nonblank equipment row. Supported categories: Mobile Phone, Laptop/PC, Other Device / Merchandise. Preserve serial numbers as strings including leading zeros. Do not invent or guess illegible values; leave them blank and add a warning. Prefer Date Received; if blank use the date next to Issued By. Dates must be DD/MM/YYYY. Preserve comments and page numbers. If no equipment rows exist, return an empty records list and the employee name if readable."""
    upload = None
    local_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temporary_pdf:
            temporary_pdf.write(pdf_bytes)
            local_path = temporary_pdf.name
        upload = client.files.upload(file=local_path, config=types.UploadFileConfig(display_name=filename))
        models = [model]
        fallback = getattr(settings, "GEMINI_FALLBACK_MODEL", "")
        if fallback and fallback != model:
            models.append(fallback)
        last_error = None
        for candidate in models:
            for attempt in range(3):
                try:
                    return client.models.generate_content(model=candidate, contents=[prompt, upload], config=types.GenerateContentConfig(response_mime_type="application/json"))
                except Exception as exc:
                    last_error = exc
                    status = getattr(getattr(exc, "response", None), "status_code", None) or getattr(exc, "code", None) or getattr(exc, "status_code", None)
                    if callable(status):
                        try:
                            status = status()
                        except Exception:
                            status = None
                    retryable_status = status in (429, 500, 502, 503, 504) or any(token in str(status).upper() for token in ("RESOURCE_EXHAUSTED", "UNAVAILABLE", "INTERNAL", "DEADLINE_EXCEEDED"))
                    if not retryable_status and attempt == 0:
                        break
                    if attempt < 2:
                        time.sleep(min(30, 2 ** attempt + random.random()))
        raise ExtractionError(f"Gemini extraction failed: {last_error}") from last_error
    finally:
        if upload is not None:
            try:
                client.files.delete(name=upload.name)
            except Exception:
                logger.warning("Could not clean up temporary Gemini file for %s", filename)
        if local_path and os.path.exists(local_path):
            os.unlink(local_path)


@transaction.atomic
def process_document(document_id, *, response_factory=None):
    document = ExtractionDocument.objects.select_for_update().select_related("batch").get(pk=document_id)
    if document.processing_status == ExtractionDocument.Status.COMPLETED:
        return document
    document.processing_status = ExtractionDocument.Status.PROCESSING
    document.processing_attempts += 1
    document.processing_started_at = timezone.now()
    document.error_message = ""
    document.save(update_fields=["processing_status", "processing_attempts", "processing_started_at", "error_message"])
    batch = document.batch
    batch.status = ExtractionBatch.Status.PROCESSING
    batch.save(update_fields=["status", "updated_at"])
    try:
        with document.stored_file.open("rb") as source_file:
            data = source_file.read()
        reader = PdfReader(BytesIO(data))
        document.page_count = len(reader.pages)
        response = response_factory(data, document.original_filename) if response_factory else _gemini_response(data, document.original_filename)
        rows = parse_extraction_response(response)
        # Replacement is transactionally safe and prevents duplicate rows on retries.
        document.records.all().delete()
        ExtractedEquipmentRecord.objects.bulk_create([
            ExtractedEquipmentRecord(batch=batch, document=document, record_index=index, employee_name=row["employee_name"], equipment_type=row["equipment_type"], make=row["make"], model=row["model"], serial_number=row["serial_number"], date_received=row["date_received"], issued_by=row["issued_by"], comments=row["comments"], page_number=row["page_number"], confidence_score=row["confidence_score"], validation_warnings=row["validation_warnings"], raw_extraction_data=row["raw_extraction_data"])
            for index, row in enumerate(rows)
        ])
        document.processing_status = ExtractionDocument.Status.COMPLETED
        document.processed_at = timezone.now()
        document.processing_started_at = None
        document.error_message = ""
    except Exception as exc:
        document.processing_status = ExtractionDocument.Status.FAILED
        document.processing_started_at = None
        document.error_message = str(exc)[:2000]
        logger.exception("Checklist extraction failed for document %s", document.pk)
    document.save(update_fields=["page_count", "processing_status", "processing_started_at", "processed_at", "error_message"])
    refresh_batch_status(batch)
    try:
        from document_processing.services.audit import record_audit
        record_audit("IMPORT" if document.processing_status == ExtractionDocument.Status.COMPLETED else "UPDATE", "ExtractionDocument", document, metadata={"status": document.processing_status})
    except Exception:
        logger.exception("Could not write extraction audit entry")
    return document


def _json_safe(row):
    return {key: (value.isoformat() if hasattr(value, "isoformat") else value) for key, value in row.items()}


def refresh_batch_status(batch):
    documents = batch.documents.all()
    total = documents.count()
    completed = documents.filter(processing_status=ExtractionDocument.Status.COMPLETED).count()
    failed = documents.filter(processing_status=ExtractionDocument.Status.FAILED).count()
    active = documents.filter(processing_status__in=[ExtractionDocument.Status.QUEUED, ExtractionDocument.Status.PROCESSING]).exists()
    if active:
        status = ExtractionBatch.Status.PROCESSING if documents.filter(processing_status=ExtractionDocument.Status.PROCESSING).exists() else ExtractionBatch.Status.UPLOADED
    elif failed and completed:
        status = ExtractionBatch.Status.PARTIAL
    elif failed:
        status = ExtractionBatch.Status.FAILED
    elif total and completed == total:
        status = ExtractionBatch.Status.REVIEW
    else:
        status = ExtractionBatch.Status.UPLOADED
    batch.status = status
    batch.save(update_fields=["status", "updated_at"])

