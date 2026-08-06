from core.docs.registry import registry


class DocumentationHomePageService:

    def build(self):

        return registry.categories()