from django.db.models import QuerySet

from assets.models import Asset
from assets.models.asset_assignment import AssetAssignment
from assets.models.asset_transfer import AssetTransfer

from django.db.models import Q, QuerySet

from assets.choices import AssignmentStatus


class AssetTransferRepository:

    # =====================================================
    # Query
    # =====================================================

    def list(
        self,
        query="",
        page=1,
        per_page=20,
    ) -> QuerySet:

        queryset = (
            AssetTransfer.objects
            .select_related(
                "company",
                "asset",
                "previous_assignment",
                "new_assignment",
                "from_employee",
                "from_site",
                "to_employee",
                "to_site",
            )
            .order_by("-transfer_date", "-created_at")
        )

        if query:

            queryset = queryset.filter(
                Q(
                    asset__asset_tag__icontains=query
                )
                |
                Q(
                    asset__serial_number__icontains=query
                )
                |
                Q(
                    to_employee__first_name__icontains=query
                )
                |
                Q(
                    to_employee__last_name__icontains=query
                )
                |
                Q(
                    to_site__name__icontains=query
                )
            )

        return queryset

    # =====================================================
    # Get
    # =====================================================

    def get(
        self,
        pk,
    ) -> AssetTransfer:

        return (
            AssetTransfer.objects
            .select_related(
                "company",
                "asset",
                "previous_assignment",
                "new_assignment",
                "from_employee",
                "from_site",
                "to_employee",
                "to_site",
            )
            .get(pk=pk)
        )

    # =====================================================
    # Active Assignment
    # =====================================================

    def get_active_assignment(
        self,
        asset: Asset,
    ) -> AssetAssignment | None:

        return (
            AssetAssignment.objects
            .select_related(
                "asset",
                "company",
                "employee",
                "site",
            )
            .filter(
                asset=asset,
                status=AssignmentStatus.ACTIVE,
            )
            .first()
        )

    # =====================================================
    # Create
    # =====================================================

    def create(
        self,
        **kwargs,
    ) -> AssetTransfer:

        return AssetTransfer.objects.create(
            **kwargs,
        )

    # =====================================================
    # Update
    # =====================================================

    def update(
        self,
        transfer: AssetTransfer,
        **kwargs,
    ) -> AssetTransfer:

        for field, value in kwargs.items():

            setattr(
                transfer,
                field,
                value,
            )

        transfer.save(
            update_fields=[
                *kwargs.keys(),
                "updated_at",
            ]
        )

        return transfer

    # =====================================================
    # Exists
    # =====================================================

    def exists(
        self,
        pk,
    ) -> bool:

        return AssetTransfer.objects.filter(
            pk=pk,
        ).exists()

    # =====================================================
    # Count
    # =====================================================

    def count(self) -> int:

        return AssetTransfer.objects.count()