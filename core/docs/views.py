from django.views.generic import TemplateView

from core.docs.page_services.documentation_page_service import (
    DocumentationPageService,
)
from django.views.generic import TemplateView

from core.docs.page_services.home_page_service import (
    DocumentationHomePageService,
)

class DocumentationView(TemplateView):

    template_name = "docs/document.html"

    page_service = DocumentationPageService()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["document"] = self.page_service.build(
            self.kwargs["slug"]
        )

        return context


class DocumentationHomeView(TemplateView):

    template_name = "docs/index.html"

    page_service = DocumentationHomePageService()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["categories"] = (
            self.page_service.build()
        )

        return context