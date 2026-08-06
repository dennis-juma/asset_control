class SearchService:

    @classmethod
    def search(
        cls,
        user,
        query,
    ):

        results = []

        for provider in SearchRegistry.providers():

            results.extend(
                provider.search(
                    user,
                    query,
                )
            )

        results.sort(
            key=lambda x: x.score,
            reverse=True,
        )

        return SearchResponseDTO(
            query=query,
            results=results,
        )