from django.db.models import Q

from assets.models import AssetHistory


class AssetHistoryRepository:
    def get(
    self,
    pk,
) -> AssetHistory:

        return (
            AssetHistory.objects
            .select_related(
                "country",
                "asset",
                "employee",
                "site",
                "performed_by",
            )
            .get(
                pk=pk,
            )   
        )

    def list(
        self,
        asset,
        query="",
        page=1,
        per_page=20,
    ):
        queryset = (
            AssetHistory.objects
            .filter(asset=asset)
            .select_related(
                "employee",
                "site",
                "performed_by",
            )
            .order_by("-event_date")
        )

        if query:
            queryset = queryset.filter(
                Q(event_type__icontains=query)
                | Q(notes__icontains=query)
                | Q(reference__icontains=query)
            )

        from django.core.paginator import Paginator

        paginator = Paginator(
            queryset,
            per_page,
        )

        return paginator.get_page(page)

    