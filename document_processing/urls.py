from django.urls import path

from document_processing.views import BatchDetailView, ExportBatchView, ExtractionDashboardView, ExtractionUploadView, PrivateDocumentView, RecordReviewView, RetryDocumentView

app_name = "document_processing"

urlpatterns = [
    path("", ExtractionDashboardView.as_view(), name="dashboard"),
    path("upload/", ExtractionUploadView.as_view(), name="upload"),
    path("batches/<uuid:batch_id>/", BatchDetailView.as_view(), name="batch-detail"),
    path("batches/<uuid:batch_id>/export/", ExportBatchView.as_view(), name="batch-export"),
    path("documents/<uuid:document_id>/", PrivateDocumentView.as_view(), name="document"),
    path("documents/<uuid:document_id>/retry/", RetryDocumentView.as_view(), name="retry-document"),
    path("records/<uuid:record_id>/", RecordReviewView.as_view(), name="record-review"),
]

