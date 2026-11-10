# Asset Document Processing

The module stores scanned equipment checklists and extracted rows in separate staging tables. It never creates assets or assignments. Original AI values remain in `raw_extraction_data`; correction history is retained in `ExtractionRecordEdit` and the shared audit log.

## Configuration

- `GEMINI_API_KEY`: Gemini API key, loaded from the environment only.
- `GEMINI_MODEL`: configured model (default: `gemini-2.5-flash`).
- `GEMINI_FALLBACK_MODEL`: optional fallback model identifier.
- PDFs are stored in `PRIVATE_MEDIA_ROOT` (default: `<project>/private_media`), outside `MEDIA_URL`.

The Google Gen AI SDK is included in `requirements.txt`; `openpyxl` and `pypdf` are also project dependencies.

## Worker and local use

For localhost development using the existing Supabase database, use the default development settings. They read the database connection from the root `.env` file:

```powershell
python manage.py runserver 127.0.0.1:8000
```

In a second terminal, start the worker with the same profile:

```powershell
python manage.py process_extraction_queue
```

The worker claims queued database rows, processes files independently, and leaves failures retryable from the batch page. Use `python manage.py process_extraction_queue --once` for one polling pass. This project has no Celery/Redis deployment; a DB-backed worker avoids adding those services. Apply the module migrations to the configured Supabase database before using the module; those migrations add the staging and audit tables without changing existing asset or assignment records.

## Access and workflow

Grant `view_extractionbatch`, `process_documents`, `review_extracted_records`, and `export_extracted_records` permissions through the existing Django permission system. Country scoped users also need access to the batch country. Upload PDFs from **Asset Management â†’ Document Processing**, review and correct extracted records, then export a batch or filtered review status to Excel.

## Deployment

Provision persistent, private storage for `PRIVATE_MEDIA_ROOT` shared by web and worker processes. Run the worker as a separately supervised process/container. Configure `GEMINI_API_KEY` in the deployment secret store, never in source control. Apply the new Django migrations during deployment. The exported workbook is for reporting/review and cannot be imported back into AMS.



