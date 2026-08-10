from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.core.exceptions import ValidationError

from assets.dtos.asset_transfer import (
    AssetTransferCreateDTO,
    AssetTransferUpdateDTO,
)

from assets.forms.transfer import (
    AssetTransferCreateForm,
    AssetTransferUpdateForm,
)

from assets.models import Asset

from assets.page_services.asset_transfer_page_service import (
    AssetTransferPageService,
)

from assets.repositories import (
    AssetRepository,
    AssetTransferRepository,
)

from assets.services.asset_transfer_service import (
    AssetTransferService,
)


class AssetTransferListView(TemplateView):

    template_name = "crud/list.html"

    def get(
        self,
        request,
        *args,
        **kwargs,
    ):

        page = AssetTransferPageService().list_page(
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



class AssetTransferCreateView(TemplateView):

    template_name = "crud/form.html"

    def get_asset(self, request):
        asset_id = request.GET.get("asset")

        if not asset_id:
            return None

        return AssetRepository().get(asset_id)

    def get(
        self,
        request,
        *args,
        **kwargs,
    ):

        asset = self.get_asset(request)

        if asset is None:
            messages.error(
                request,
                "Please select an asset before starting a transfer.",
            )

            return redirect(
                "assets:asset-list",
            )

        previous_assignment = (
            AssetTransferRepository()
            .get_active_assignment(asset)
        )

        if previous_assignment is None:
            messages.error(
                request,
                "This asset does not have an active assignment.",
            )

            return redirect(
                "assets:asset-detail",
                pk=asset.pk,
            )

        page = AssetTransferPageService().create_page(
            asset=asset,
            previous_assignment=previous_assignment,
        )

        return self.render_to_response(
            {
                "page": page,
            }
        )

    def post(
        self,
        request,
        *args,
        **kwargs,
    ):

        asset = self.get_asset(request)

        if asset is None:
            messages.error(
                request,
                "Please select an asset before starting a transfer.",
            )

            return redirect(
                "assets:asset-list",
            )

        previous_assignment = (
            AssetTransferRepository()
            .get_active_assignment(asset)
        )

        if previous_assignment is None:
            messages.error(
                request,
                "This asset does not have an active assignment.",
            )

            return redirect(
                "assets:asset-detail",
                pk=asset.pk,
            )

        form = AssetTransferCreateForm(
            request.POST,
            asset=asset,
            previous_assignment=previous_assignment,
        )

        if not form.is_valid():

            return self.render_to_response(
                {
                    "page":
                    AssetTransferPageService().create_page(
                        form=form,
                        asset=asset,
                        previous_assignment=previous_assignment,
                    ),
                }
            )

        dto = AssetTransferCreateDTO(
            company=asset.company,
            asset=asset,
            previous_assignment=previous_assignment,
            to_employee=form.cleaned_data.get(
                "employee",
            ),
            to_site=form.cleaned_data.get(
                "site",
            ),
            transfer_date=form.cleaned_data.get(
                "transfer_date",
            ),
            reason=form.cleaned_data.get(
                "reason",
            ),
            remarks=form.cleaned_data.get(
                "remarks",
            ),
        )

        try:

                AssetTransferService().create(dto)

        except ValidationError as exc:
            if hasattr(exc, "message_dict"):

                    for field, errors in exc.message_dict.items():

                        for error in errors:

                            messages.error(
                                request,
                                error,
                            )

            else:

                    messages.error(
                        request,
                        str(exc),
                    )

            return self.render_to_response(
                    {
                        "page":
                        AssetTransferPageService().create_page(
                            form=form,
                            asset=asset,
                            previous_assignment=previous_assignment,
                        ),
                    }
                )

        messages.success(
                        request,
                        "Asset transferred successfully.",
                    )

        return redirect(
                        "assets:asset-transfer-list",
                    )


class AssetTransferDetailView(TemplateView):

    template_name = "crud/form.html"

    def get(
        self,
        request,
        pk,
        *args,
        **kwargs,
    ):

        transfer = AssetTransferRepository().get(
            pk,
        )

        page = (
            AssetTransferPageService()
            .detail_page(
                transfer,
            )
        )

        return self.render_to_response(
            {
                "page": page,
            }
        )


class AssetTransferUpdateView(TemplateView):

    template_name = "crud/form.html"

    def get(
        self,
        request,
        pk,
        *args,
        **kwargs,
    ):

        transfer = AssetTransferRepository().get(
            pk,
        )

        page = (
            AssetTransferPageService()
            .update_page(
                transfer,
            )
        )

        return self.render_to_response(
            {
                "page": page,
            }
        )

    def post(
        self,
        request,
        pk,
        *args,
        **kwargs,
    ):

        transfer = AssetTransferRepository().get(
            pk,
        )

        form = AssetTransferUpdateForm(
            request.POST,
            instance=transfer,
        )

        if not form.is_valid():

            return self.render_to_response(
                {
                    "page":
                    AssetTransferPageService().update_page(
                        transfer,
                        form,
                    ),
                }
            )

        dto = AssetTransferUpdateDTO(
            transfer_date=form.cleaned_data.get(
                "transfer_date",
            ),
            reason=form.cleaned_data.get(
                "reason",
            ),
            remarks=form.cleaned_data.get(
                "remarks",
            ),
            is_active=form.cleaned_data.get(
                "is_active",
            ),
        )

        AssetTransferService().update(
            transfer,
            dto,
        )

        messages.success(
            request,
            "Transfer updated successfully.",
        )

        return redirect(
            "assets:asset-transfer-detail",
            pk=transfer.pk,
        )