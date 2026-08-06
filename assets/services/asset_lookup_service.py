from organizations.models import Company
from assets.models import AssetCategory
from assets.choices.choices import AssetStatus


class AssetLookupService:
    """
    Provides lookup data for Asset screens.
    """

    def get_filters(self):

        return {
            "asset_statuses": AssetStatus.choices,
            "companies": Company.objects.order_by("name"),
            "categories": AssetCategory.objects.order_by("name"),
        }