class AssetPolicy:

    @staticmethod
    def can_edit(
        user,
        asset,
    ):

        if user.is_superuser:

            return True

        if asset.site == user.site:

            return True

        return False