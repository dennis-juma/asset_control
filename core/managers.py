from django.db import models


class ActiveManager(models.Manager):
    """
    Returns only active (non-deleted) records.
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class DeletedManager(models.Manager):
    """
    Returns only deleted records.
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)


class AllObjectsManager(models.Manager):
    """
    Returns every record including soft deleted.
    """

    def get_queryset(self):
        return super().get_queryset()