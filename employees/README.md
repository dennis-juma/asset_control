# Scheduled employee offboarding

Celery Beat schedules the offboarding scan daily at 08:00 in `TIME_ZONE` (the default is `Africa/Dar_es_Salaam`, EAT). The scan queues active employees whose `last_working_date` is today or earlier, so a temporary scheduler outage does not skip an exit. Each employee task locks and rechecks the employee row to prevent duplicate notices when tasks overlap.

The task sends the existing asset return email (including currently assigned assets), deactivates the employee and linked AMS account, and writes an `Employee` audit entry. Email failures roll back the database changes and are retried with backoff. The broker is Redis, configured with `CELERY_BROKER_URL`; no application database migration is needed.

## Local Windows setup

Install the project dependencies and make sure Redis is running at `127.0.0.1:6379` (or set `CELERY_BROKER_URL` in `.env` to your Redis URL). Run the web server, worker, and Beat scheduler in separate PowerShell windows from the project folder:

```powershell
.\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

```powershell
.\venv\Scripts\python.exe -m celery -A config worker --loglevel=INFO --pool=solo
```

```powershell
.\venv\Scripts\python.exe -m celery -A config beat --loglevel=INFO --schedule=celerybeat-schedule
```

On Linux, run the worker without `--pool=solo`. Keep exactly one Beat scheduler running for this schedule.

## AWS Compose deployment

`compose.aws.yml` runs a Redis broker, one Celery worker, and one Beat scheduler alongside the web service. Deploy the updated image and Compose configuration together. The web application and workers use the same `.env` settings and Supabase database; Compose overrides the broker URL to use its internal Redis service.
