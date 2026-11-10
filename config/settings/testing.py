from .base import *

DEBUG = False

# Tests must never connect to the configured Supabase or production database.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Some historical production migrations rely on PostgreSQL-only schema behavior;
# build the test schema from current models instead.
MIGRATION_MODULES = {
    app: None
    for app in [
        "accounts", "assets", "auditlogs", "core", "dashboard",
        "document_processing", "employees", "maintenance", "notifications",
        "organizations", "reports", "vendors",
    ]
}

STORAGES = {
    **STORAGES,
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
