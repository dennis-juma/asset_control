from core.badges.registry import BadgeRegistry


class BadgeService:

    @staticmethod
    def asset(status):
        return BadgeRegistry.asset.build(status)

    @staticmethod
    def boolean(value):
        return BadgeRegistry.boolean.build(value)

    @staticmethod
    def warranty(expiry):
        return BadgeRegistry.warranty.build(expiry)