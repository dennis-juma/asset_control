import importlib

from django.http import Http404

from core.docs.registry import registry


class DocumentationPageService:

    def build(self, slug):

        metadata = registry.get(slug)

        if metadata is None:
            raise Http404("Document not found.")

        module = importlib.import_module(
            metadata.module
        )

        return module.build()