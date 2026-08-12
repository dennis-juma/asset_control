from typing import Optional


from django.db import transaction
from assets.models import Asset, AssetHistory
from django.contrib.auth.models import AbstractBaseUser
from employees.models import Employee
from organizations.models import Site



class AssetHistoryService:
    """
    Central service for recording asset lifecycle events.

    This service should be the ONLY place where AssetHistory
    records are created.
    """

    @staticmethod
    @transaction.atomic
    def log_event(
        *,
        asset: Asset,
        event_type: str,
        performed_by: Optional[AbstractBaseUser] = None,
        employee: Optional[Employee] = None,
        site: Optional[Site] = None,
        old_status: Optional[str] = None,
        new_status: Optional[str] = None,
        reference: str = "",
        notes: str = "",
        metadata: Optional[dict] = None,
    ) -> AssetHistory:

        return AssetHistory.objects.create(
            country=asset.country,
            asset=asset,
            event_type=event_type,
            performed_by=performed_by,
            employee=employee,
            site=site,
            old_status=old_status or "",
            new_status=new_status or "",
            reference=reference,
            notes=notes,
            metadata=metadata or {},
        )


    @staticmethod
    @transaction.atomic
    def log_events(events: list[dict]) -> list[AssetHistory]:
        """
        Bulk create history records.

        Example:
            AssetHistoryService.log_events([
                {...},
                {...},
            ])
        """

    

        return [
    AssetHistoryService.log_event(**event)
    for event in events
]