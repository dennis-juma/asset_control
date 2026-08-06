from django.views.generic import TemplateView
from .page_services.datagrid_page_service import (
    DataGridPageService,
)
from .registry import UI_COMPONENTS


class UIHomeView(TemplateView):
    template_name = "ui/index.html"

    extra_context = {
        "components": UI_COMPONENTS,
    }


class DataGridDemoView(TemplateView):

    template_name = "ui/datagrid.html"



class DataGridDemoView(TemplateView):

    template_name = "playground/datagrid.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["page"] = DataGridPageService().build()

        return context



    