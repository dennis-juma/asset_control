from django.views.generic import TemplateView
from core.permissions.constants import Permissions
from core.permissions.mixins import PermissionRequiredMixin

from assets.repositories import (
    AssetRepository,
    AssetHistoryRepository,
)

from assets.page_services import (
    AssetHistoryPageService,
)


class AssetHistoryListView(
     PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_VIEW

    template_name = "crud/list.html"

    def get(
        self,
        request,
        pk,
        *args,
        **kwargs,
    ):

        asset = AssetRepository().get(pk)

        page = AssetHistoryPageService().list_page(
            asset=asset,
            query=request.GET.get(
                "q",
                "",
            ),
            page=request.GET.get(
                "page",
                1,
            ),
        )

        return self.render_to_response(
            {
                "page": page,
            }
        )


class AssetHistoryDetailView(
     PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_VIEW
    template_name = "crud/form.html"

    def get(
        self,
        request,
        pk,
        *args,
        **kwargs,
    ):

        history = AssetHistoryRepository().get(pk)

        page = AssetHistoryPageService().detail_page(
            history=history,
        )

        return self.render_to_response(
            {
                "page": page,
            }
        )           