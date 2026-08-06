class DashboardService:

    def __init__(
        self,
        provider,
    ):

        self.provider = provider

    def build(self):

        return self.provider.build()