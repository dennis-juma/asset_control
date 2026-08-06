from datetime import date

from core.badges.base import BadgeProvider
from core.badges.enums import BadgeColor
from core.dtos.badge import BadgeDTO


class WarrantyBadge(BadgeProvider):

    def build(self, expiry_date):

        if expiry_date is None:
            return BadgeDTO(
                text="No Warranty",
                color=BadgeColor.SECONDARY,
            )

        days = (expiry_date - date.today()).days

        if days < 0:
            return BadgeDTO(
                text="Expired",
                color=BadgeColor.DANGER,
            )

        if days <= 30:
            return BadgeDTO(
                text="Expires Soon",
                color=BadgeColor.WARNING,
            )

        return BadgeDTO(
            text="Active",
            color=BadgeColor.SUCCESS,
        )