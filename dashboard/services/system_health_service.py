from django.conf import settings
from django.core.cache import cache
from django.db import connection
from dashboard.dto.system_health_service import (
    HealthItemDTO,
    SystemHealthDTO,
)


class SystemHealthService:
    """
    Provides dashboard system health information.
    """

    def get_health(self) -> SystemHealthDTO:
        return SystemHealthDTO(
            items=[
                self._database_health(),
                self._redis_health(),
                self._storage_health(),
            ],
            last_backup=self._last_backup(),
            version=self._version(),
        )

    def _database_health(self) -> HealthItemDTO:
        try:
            connection.ensure_connection()

            return HealthItemDTO(
                title="Database",
                status="Healthy",
                icon="bi bi-database",
                color="success",
            )

        except Exception:
            return HealthItemDTO(
                title="Database",
                status="Offline",
                icon="bi bi-database",
                color="danger",
            )

    def _redis_health(self) -> HealthItemDTO:
        try:
            cache.set("__health__", "ok", timeout=5)

            if cache.get("__health__") == "ok":
                return HealthItemDTO(
                    title="Redis",
                    status="Healthy",
                    icon="bi bi-lightning-charge",
                    color="success",
                )

        except Exception:
            pass

        return HealthItemDTO(
            title="Redis",
            status="Unavailable",
            icon="bi bi-lightning-charge",
            color="danger",
        )

    def _storage_health(self) -> HealthItemDTO:
        """
        Placeholder implementation.
        Replace later with S3/local storage health check.
        """

        return HealthItemDTO(
            title="Storage",
            status="Healthy",
            icon="bi bi-hdd-network",
            color="success",
        )

    def _last_backup(self) -> str:
        """
        Placeholder until backup scheduler is implemented.
        """
        return "2 hours ago"

    def _version(self) -> str:
        return getattr(settings, "APP_VERSION", "1.0.0")