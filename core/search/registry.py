class SearchRegistry:

    PROVIDERS = []

    @classmethod
    def register(
        cls,
        provider,
    ):

        cls.PROVIDERS.append(provider)

    @classmethod
    def providers(cls):

        return cls.PROVIDERS