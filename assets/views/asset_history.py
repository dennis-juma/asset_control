from django.views.generic import TemplateView

from assets.repositories import (
    AssetRepository,
)

from assets.page_services import (
    AssetHistoryPageService,
)


class AssetHistoryListView(TemplateView):

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