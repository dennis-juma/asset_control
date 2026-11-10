from django.contrib import admin

from document_processing.models import ExtractionBatch, ExtractionDocument, ExtractionRecordEdit, ExtractedEquipmentRecord


class ExtractionDocumentInline(admin.TabularInline):
    model = ExtractionDocument
    extra = 0
    readonly_fields = ("original_filename", "file_size", "processing_status", "processing_attempts", "error_message", "uploaded_at", "processed_at")
    can_delete = False


@admin.register(ExtractionBatch)
class ExtractionBatchAdmin(admin.ModelAdmin):
    list_display = ("batch_number", "name", "country", "status", "uploaded_by", "uploaded_at")
    list_filter = ("status", "country")
    search_fields = ("batch_number", "name")
    readonly_fields = ("batch_number", "uploaded_at", "created_at", "updated_at")
    inlines = (ExtractionDocumentInline,)


@admin.register(ExtractionDocument)
class ExtractionDocumentAdmin(admin.ModelAdmin):
    list_display = ("original_filename", "batch", "processing_status", "processing_attempts", "uploaded_at")
    list_filter = ("processing_status",)
    search_fields = ("original_filename", "sha256", "batch__batch_number")
    readonly_fields = ("original_filename", "sha256", "file_size", "page_count", "processing_attempts", "uploaded_at", "processed_at")
    exclude = ("stored_file",)


@admin.register(ExtractedEquipmentRecord)
class ExtractedEquipmentRecordAdmin(admin.ModelAdmin):
    list_display = ("employee_name", "equipment_type", "serial_number", "review_status", "batch")
    list_filter = ("review_status", "equipment_type")
    search_fields = ("employee_name", "serial_number", "batch__batch_number")
    readonly_fields = ("raw_extraction_data", "created_at", "updated_at")


@admin.register(ExtractionRecordEdit)
class ExtractionRecordEditAdmin(admin.ModelAdmin):
    list_display = ("record", "edited_by", "edited_at")
    readonly_fields = ("record", "edited_by", "before", "after", "edited_at")

