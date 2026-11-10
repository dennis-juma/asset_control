import time
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from document_processing.models import ExtractionDocument
from document_processing.services.extraction import process_document


class Command(BaseCommand):
    help = "Process queued employee equipment checklist PDFs. Run as a separate long-lived worker."

    def add_arguments(self, parser):
        parser.add_argument("--once", action="store_true", help="Process available queued documents once, then exit.")
        parser.add_argument("--poll-seconds", type=float, default=3.0)

    def handle(self, *args, **options):
        once = options["once"]
        while True:
            document_id = None
            with transaction.atomic():
                stale_before = timezone.now() - timedelta(minutes=30)
                candidate = ExtractionDocument.objects.filter(
                    Q(processing_status=ExtractionDocument.Status.QUEUED)
                    | Q(processing_status=ExtractionDocument.Status.PROCESSING, processing_started_at__lt=stale_before)
                    | Q(processing_status=ExtractionDocument.Status.PROCESSING, processing_started_at__isnull=True)
                ).order_by("uploaded_at").select_for_update(skip_locked=True).first()
                if candidate:
                    candidate.processing_status = ExtractionDocument.Status.PROCESSING
                    candidate.processing_started_at = timezone.now()
                    candidate.save(update_fields=["processing_status", "processing_started_at"])
                    document_id = candidate.pk
            if document_id:
                result = process_document(document_id)
                self.stdout.write(f"{result.original_filename}: {result.processing_status}")
            elif once:
                break
            else:
                time.sleep(options["poll_seconds"])

