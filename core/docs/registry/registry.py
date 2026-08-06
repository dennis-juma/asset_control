

from .document import DocumentMetadata


class DocumentationRegistry:

    def __init__(self):

        self._documents = {}

    def register(
        self,
        document: DocumentMetadata,
    ):

        self._documents[
            document.slug
        ] = document

    def get(
        self,
        slug: str,
    ):

        return self._documents.get(slug)

    def all(self):

        return list(
            self._documents.values()
        )

    def categories(self):

        categories = {}

        for document in self._documents.values():

            categories.setdefault(
                document.category,
                []
            ).append(document)

        return categories


    def __init__(self):
        self._documents = {}

    def register(self, document: DocumentMetadata):
        self._documents[document.slug] = document

    def get(self, slug: str):
        return self._documents.get(slug)

    def all(self):
        return list(self._documents.values())

    def categories(self):
        categories = {}

        for document in self._documents.values():
            categories.setdefault(
                document.category,
                []
            ).append(document)

        return categories


# Create the singleton registry
registry = DocumentationRegistry()

