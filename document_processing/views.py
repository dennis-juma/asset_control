import hashlib
import os

from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError, transaction
from django.db.models import Count, Q
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from core.permissions.constants import Permissions
from core.permissions.mixins import PermissionRequiredMixin
from document_processing.forms import ExtractedEquipmentRecordForm, UploadDocumentsForm
from document_processing.models import ExtractionBatch, ExtractionDocument, ExtractionRecordEdit, ExtractedEquipmentRecord
from document_processing.services.audit import record_audit
from document_processing.services.extraction import refresh_batch_status
from document_processing.services.export import export_records


class ExtractionDashboardView(PermissionRequiredMixin, TemplateView):
    template_name = "document_processing/dashboard.html"
    permission_required = Permissions.DOCUMENT_VIEW

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        batches = ExtractionBatch.objects.select_related("uploaded_by", "country")
        records = ExtractedEquipmentRecord.objects.all()
        if not self.request.user.is_superuser and self.request.user.user_type != "SUPER_ADMIN":
            from core.services.country_context import CountryContextService
            accessible_countries = CountryContextService.get_available_countries(self.request.user)
            batches = batches.filter(country__in=accessible_countries)
            records = records.filter(batch__country__in=accessible_countries)
        documents = ExtractionDocument.objects.filter(batch__in=batches)
        context.update({"batches": batches[:15], "batch_count": batches.count(), "document_count": documents.count(), "record_count": records.count(), "pending_count": records.filter(review_status=ExtractedEquipmentRecord.ReviewStatus.PENDING).count(), "reviewed_count": records.filter(review_status=ExtractedEquipmentRecord.ReviewStatus.REVIEWED).count(), "failed_count": documents.filter(processing_status=ExtractionDocument.Status.FAILED).count()})
        return context


class ExtractionUploadView(PermissionRequiredMixin, View):
    permission_required = Permissions.DOCUMENT_PROCESS
    template_name = "document_processing/upload.html"

    def get(self, request):
        initial = {}
        if getattr(request, "country_context", None) and request.country_context.country:
            initial["country"] = request.country_context.country.pk
        return render(request, self.template_name, {"form": UploadDocumentsForm(user=request.user, initial=initial)})

    def post(self, request):
        form = UploadDocumentsForm(request.POST, request.FILES, user=request.user)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})
        country, site = form.cleaned_data["country"], form.cleaned_data["site"]
        if country and not _can_access_country(request.user, country):
            raise PermissionDenied
        if site and not _can_access_country(request.user, site.country):
            raise PermissionDenied
        files = request.FILES.getlist("files")
        with transaction.atomic():
            batch = ExtractionBatch.objects.create(name=form.cleaned_data["name"], country=country or (site.country if site else None), site=site, uploaded_by=request.user)
            seen = set()
            for uploaded in files:
                try:
                    digest = hashlib.sha256(uploaded.read()).hexdigest()
                    uploaded.seek(0)
                    if digest in seen:
                        messages.warning(request, f"Skipped duplicate file {uploaded.name}.")
                        continue
                    seen.add(digest)
                    if ExtractionDocument.objects.filter(batch__country=batch.country, sha256=digest).exists():
                        messages.warning(request, f"Skipped previously uploaded file {uploaded.name}.")
                        continue
                    document = ExtractionDocument(batch=batch, original_filename=os.path.basename(uploaded.name)[:255], file_size=uploaded.size, sha256=digest)
                    document.stored_file.save(uploaded.name, uploaded, save=False)
                    document.full_clean()
                    document.save()
                finally:
                    uploaded.close()
        if not batch.documents.exists():
            batch.delete()
            messages.error(request, "No new documents were uploaded.")
            return redirect("document_processing:upload")
        record_audit("IMPORT", "ExtractionBatch", batch, user=request.user, metadata={"documents": batch.total_files})
        messages.success(request, f"Batch {batch.batch_number} queued with {batch.total_files} PDF(s). Extraction runs in the background.")
        return redirect("document_processing:batch-detail", batch_id=batch.pk)


class BatchDetailView(PermissionRequiredMixin, TemplateView):
    template_name = "document_processing/batch_detail.html"
    permission_required = Permissions.DOCUMENT_VIEW

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        batch = get_object_or_404(ExtractionBatch.objects.select_related("uploaded_by", "country", "site"), pk=kwargs["batch_id"])
        _ensure_country_access(self.request.user, batch.country)
        documents = batch.documents.all()
        records = batch.records.select_related("document").all()
        query = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("equipment_type", "")
        review_status = self.request.GET.get("review_status", "")
        if query:
            records = records.filter(Q(employee_name__icontains=query) | Q(serial_number__icontains=query) | Q(make__icontains=query) | Q(model__icontains=query))
        if category:
            records = records.filter(equipment_type=category)
        if review_status:
            records = records.filter(review_status=review_status)
        sort = self.request.GET.get("sort", "employee_name")
        if sort.lstrip("-") not in {"employee_name", "equipment_type", "serial_number", "date_received", "review_status"}:
            sort = "employee_name"
        records = records.order_by(sort, "id")
        page = Paginator(records, 25).get_page(self.request.GET.get("page"))
        completed_documents = batch.documents.filter(processing_status__in=[ExtractionDocument.Status.COMPLETED, ExtractionDocument.Status.FAILED]).count()
        progress_percent = round(100 * completed_documents / batch.total_files) if batch.total_files else 0
        context.update({"batch": batch, "documents": documents, "records": page, "page_obj": page, "query": query, "category": category, "review_status": review_status, "sort": sort, "progress_percent": progress_percent, "completed_documents": completed_documents})
        return context


class RecordReviewView(PermissionRequiredMixin, View):
    permission_required = Permissions.DOCUMENT_REVIEW
    template_name = "document_processing/review.html"

    def get(self, request, record_id):
        record = get_object_or_404(ExtractedEquipmentRecord.objects.select_related("batch", "document"), pk=record_id)
        _ensure_country_access(request.user, record.batch.country)
        form = ExtractedEquipmentRecordForm(instance=record)
        siblings = record.batch.records.order_by("document__uploaded_at", "record_index")
        return render(request, self.template_name, {"record": record, "form": form, "siblings": siblings})

    def post(self, request, record_id):
        record = get_object_or_404(ExtractedEquipmentRecord.objects.select_related("batch", "document"), pk=record_id)
        _ensure_country_access(request.user, record.batch.country)
        review_status_before = record.review_status
        fields = ["employee_name", "equipment_type", "make", "model", "serial_number", "date_received", "issued_by", "comments", "review_comments", "flagged_for_review"]
        before = {key: (getattr(record, key).isoformat() if getattr(record, key) else "") if key == "date_received" else getattr(record, key) for key in fields}
        form = ExtractedEquipmentRecordForm(request.POST, instance=record)
        action = request.POST.get("action", "save")
        if form.is_valid():
            with transaction.atomic():
                updated = form.save(commit=False)
                updated.updated_at = timezone.now()
                if action == "review":
                    updated.review_status = ExtractedEquipmentRecord.ReviewStatus.REVIEWED
                    updated.reviewed_by = request.user
                    updated.reviewed_at = timezone.now()
                elif action == "unreview":
                    updated.review_status = ExtractedEquipmentRecord.ReviewStatus.PENDING
                    updated.reviewed_by = None
                    updated.reviewed_at = None
                updated.save()
                after = {key: (getattr(updated, key).isoformat() if getattr(updated, key) else "") if key == "date_received" else getattr(updated, key) for key in fields}
                if before != after:
                    ExtractionRecordEdit.objects.create(record=updated, edited_by=request.user, before=before, after=after)
                    record_audit("UPDATE", "ExtractedEquipmentRecord", updated, user=request.user, before=before, after=after)
                if action in ("review", "unreview"):
                    record_audit("UPDATE", "ExtractedEquipmentRecord", updated, user=request.user, before={"review_status": review_status_before}, after={"review_status": updated.review_status}, metadata={"reviewed_at": updated.reviewed_at.isoformat() if updated.reviewed_at else None})
            if action in ("review", "unreview"):
                messages.success(request, "Record review status updated.")
            else:
                messages.success(request, "Corrections saved.")
            return redirect("document_processing:record-review", record_id=record.pk)
        return render(request, self.template_name, {"record": record, "form": form, "siblings": record.batch.records.order_by("document__uploaded_at", "record_index")})


class PrivateDocumentView(PermissionRequiredMixin, View):
    permission_required = Permissions.DOCUMENT_VIEW

    def get(self, request, document_id):
        document = get_object_or_404(ExtractionDocument.objects.select_related("batch"), pk=document_id)
        _ensure_country_access(request.user, document.batch.country)
        try:
            file_handle = document.stored_file.open("rb")
        except (FileNotFoundError, ValueError):
            raise Http404
        return FileResponse(file_handle, content_type="application/pdf", filename=document.original_filename, as_attachment=False)


class RetryDocumentView(PermissionRequiredMixin, View):
    permission_required = Permissions.DOCUMENT_PROCESS

    def post(self, request, document_id):
        document = get_object_or_404(ExtractionDocument.objects.select_related("batch"), pk=document_id)
        _ensure_country_access(request.user, document.batch.country)
        if document.processing_status != ExtractionDocument.Status.COMPLETED:
            document.processing_status = ExtractionDocument.Status.QUEUED
            document.error_message = ""
            document.save(update_fields=["processing_status", "error_message"])
            refresh_batch_status(document.batch)
            messages.success(request, f"{document.original_filename} queued for retry.")
        return redirect("document_processing:batch-detail", batch_id=document.batch_id)


class ExportBatchView(PermissionRequiredMixin, View):
    permission_required = Permissions.DOCUMENT_EXPORT

    def get(self, request, batch_id):
        batch = get_object_or_404(ExtractionBatch, pk=batch_id)
        _ensure_country_access(request.user, batch.country)
        records = batch.records.select_related("batch", "document")
        status = request.GET.get("review_status")
        if status in ExtractedEquipmentRecord.ReviewStatus.values:
            records = records.filter(review_status=status)
        category = request.GET.get("equipment_type", "")
        query = request.GET.get("q", "").strip()
        if category:
            records = records.filter(equipment_type=category)
        if query:
            records = records.filter(Q(employee_name__icontains=query) | Q(serial_number__icontains=query))
        record_audit("EXPORT", "ExtractionBatch", batch, user=request.user, metadata={"count": records.count(), "review_status": status or "all"})
        return export_records(records)


def _can_access_country(user, country):
    if user.is_superuser:
        return True
    from core.services.country_context import CountryContextService
    return CountryContextService.can_access_country(user, country)


def _ensure_country_access(user, country):
    if country and not _can_access_country(user, country):
        raise PermissionDenied

