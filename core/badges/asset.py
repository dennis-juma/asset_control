from core.badges.base import BadgeProvider
from core.badges.enums import BadgeColor
from core.dtos.badge import BadgeDTO


class AssetStatusBadge(BadgeProvider):

    COLORS = {
        "AVAILABLE": BadgeColor.SUCCESS,
        "ASSIGNED": BadgeColor.PRIMARY,
        "MAINTENANCE": BadgeColor.WARNING,
        "RETIRED": BadgeColor.DANGER,
        "LOST": BadgeColor.DARK,
    }

    ICONS = {
        "AVAILABLE": "bi-check-circle",
        "ASSIGNED": "bi-person-check",
        "MAINTENANCE": "bi-tools",
        "RETIRED": "bi-trash",
        "LOST": "bi-exclamation-octagon",
    }

    def build(self, status):

        return BadgeDTO(
            text=status.replace("_", " ").title(),
            color=self.COLORS[status],
            icon=self.ICONS[status],
        )