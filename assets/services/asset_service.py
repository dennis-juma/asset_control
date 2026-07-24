from __future__ import annotations

from typing import Any, Optional

from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import transaction

from assets.choices.history_choices import AssetHistoryEvent
from assets.models import Asset
from assets.services.asset_history_service import AssetHistoryService
from employees.models import Employee
from organizations.models import Site


class AssetService:
    """
    Business logic for Asset operations.

    All asset creation, updates and lifecycle operations
    should pass through this service.
    """

    @staticmethod
    @transaction.atomic
    def create_asset(
        *,
        asset_data: dict[str, Any],
        performed_by: Optional[AbstractBaseUser] = None,
    ) -> Asset:
        """
        Create a new asset.
        """

        asset = Asset(**asset_data)

        AssetService._save_asset(asset)

        AssetService._log_history(
            asset=asset,
            event_type=AssetHistoryEvent.CREATED,
            performed_by=performed_by,
            new_status=asset.status,
            notes="Asset created.",
        )

        return asset
    



    @staticmethod
    @transaction.atomic
    def update_asset(
        *,
        asset: Asset,
        asset_data: dict[str, Any],
        performed_by: Optional[AbstractBaseUser] = None,
    ) -> Asset:
        """
        Update asset information.
        """

        previous_status = asset.status

        for field, value in asset_data.items():

            if not hasattr(asset, field):
                raise AttributeError(
                    f"Asset has no field named '{field}'."
                )

            setattr(asset, field, value)

        AssetService._save_asset(asset)
        if previous_status != asset.status:

            AssetService._log_history(
                asset=asset,
                event_type=AssetHistoryEvent.STATUS_CHANGED,
                performed_by=performed_by,
                old_status=previous_status,
                new_status=asset.status,
                notes="Asset status updated.",
            )

        return asset

    @staticmethod
    @transaction.atomic
    def change_status(
        *,
        asset: Asset,
        new_status: str,
        performed_by: Optional[AbstractBaseUser] = None,
        employee: Optional[Employee] = None,
        site: Optional[Site] = None,
        reference: str = "",
        notes: str = "",
        metadata: Optional[dict[str, Any]] = None,
    ) -> Asset:
        """
        Change an asset's lifecycle status.
        """

        AssetService._validate_status_transition(
        asset=asset,
        new_status=new_status,
    )

        old_status = asset.status

        asset.status = new_status
        AssetService._save_asset(asset)
        AssetService._log_history(
            asset=asset,
            event_type=AssetHistoryEvent.STATUS_CHANGED,
            performed_by=performed_by,
            employee=employee,
            site=site,
            old_status=old_status,
            new_status=new_status,
            reference=reference,
            notes=notes or "Asset status changed.",
            metadata=metadata,
        )

        return asset
    

    @staticmethod
    def _log_history(
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
        metadata: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Record an asset history event.
        """

        AssetHistoryService.log_event(
            asset=asset,
            event_type=event_type,
            performed_by=performed_by,
            employee=employee,
            site=site,
            old_status=old_status,
            new_status=new_status,
            reference=reference,
            notes=notes,
            metadata=metadata,
        )


    @staticmethod
    def _save_asset(asset: Asset) -> None:
        """
        Validate and save an asset.
        """
        asset.full_clean()
        asset.save()