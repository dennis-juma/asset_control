from django.core.paginator import Paginator
from django.db.models import Q, QuerySet

from assets.models import Asset
from assets.choices.choices import AssetStatus


class AssetRepository:
    """
    Repository responsible for Asset database operations.
    """

    def get_queryset(self) -> QuerySet:
        return (
            Asset.objects.select_related(
                "company",
                "category",
                "brand",
                "model",
                "vendor",
                "currency",
            )
            .all()
        )

    def search(self, queryset: QuerySet, search: str) -> QuerySet:
        if not search:
            return queryset

        return queryset.filter(
            Q(asset_tag__icontains=search)
            | Q(serial_number__icontains=search)
            | Q(barcode__icontains=search)
            | Q(model__name__icontains=search)
            | Q(brand__name__icontains=search)
        )

    def filter(
        self,
        queryset: QuerySet,
        *,
        company=None,
        category=None,
        status=None,
    ) -> QuerySet:

        if company:
            queryset = queryset.filter(company_id=company)

        if category:
            queryset = queryset.filter(category_id=category)

        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def order(self, queryset: QuerySet, ordering: str) -> QuerySet:

        allowed = {
            "asset_tag",
            "-asset_tag",
            "purchase_date",
            "-purchase_date",
            "created_at",
            "-created_at",
            "status",
            "-status",
        }

        if ordering not in allowed:
            ordering = "-created_at"

        return queryset.order_by(ordering)

    def paginate(self, queryset: QuerySet, page: int, page_size: int = 25):
        paginator = Paginator(queryset, page_size)
        return paginator.get_page(page)

    def statistics(self):

        return {
            "total": Asset.objects.count(),
            "assigned": Asset.objects.filter(
                status=AssetStatus.ASSIGNED
            ).count(),
            "in_stock": Asset.objects.filter(
                status=AssetStatus.IN_STOCK
            ).count(),
            "maintenance": Asset.objects.filter(
                status=AssetStatus.MAINTENANCE
            ).count(),
            "retired": Asset.objects.filter(
                status=AssetStatus.RETIRED
            ).count(),
        }