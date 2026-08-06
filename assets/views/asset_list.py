from django.views.generic import TemplateView

from assets.services.asset_list_service import AssetListService
from assets.services.asset_lookup_service import AssetLookupService


class AssetListView(TemplateView):
    template_name = "assets/list.html"

    service_class = AssetListService
    lookup_service_class = AssetLookupService

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.service = self.service_class()
        self.lookup_service = self.lookup_service_class()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["asset_list"] = self.service.get_asset_list(self.request)
        context.update(self.lookup_service.get_context())

        return context