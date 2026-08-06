from core.badges.base import BadgeProvider
from core.badges.enums import BadgeColor
from core.dtos.badge import BadgeDTO


class BooleanBadge(BadgeProvider):

    def build(self, value):

        return BadgeDTO(
            text="Yes" if value else "No",
            color=BadgeColor.SUCCESS if value else BadgeColor.SECONDARY,
            icon="bi-check-circle" if value else "bi-x-circle",
        )