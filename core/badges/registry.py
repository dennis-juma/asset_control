from core.badges.asset import AssetStatusBadge
from core.badges.boolean import BooleanBadge
from core.badges.warranty import WarrantyBadge


class BadgeRegistry:

    asset = AssetStatusBadge()

    boolean = BooleanBadge()

    warranty = WarrantyBadge()