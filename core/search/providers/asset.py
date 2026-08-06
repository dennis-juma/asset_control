class AssetSearchProvider(BaseSearchProvider):

    def search(
        self,
        user,
        query,
    ):

        assets = (
            AssetRepository.visible_to(user)
            .search(query)
        )

        return [
            SearchResultDTO(
                result_type=SearchResultType.ASSET,
                title=asset.asset_tag,
                subtitle=asset.name,
                url=reverse(
                    "assets:detail",
                    args=[asset.id],
                ),
                icon="bi-laptop",
            )
            for asset in assets
        ]