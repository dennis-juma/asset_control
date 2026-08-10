from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView

from assets.dtos import (
    AssetCreateDTO,
    AssetUpdateDTO,
)
from assets.forms import (
    AssetCreateForm,
    AssetUpdateForm,
)
from assets.page_services import AssetPageService
from assets.repositories import AssetRepository
from assets.services import AssetService


class AssetListView(TemplateView):

    template_name = "crud/list.html"

    def get(self, request, *args, **kwargs):

        page = AssetPageService().list_page(
            query=request.GET.get("q", ""),
            page=request.GET.get("page", 1),
        )

        return self.render_to_response(
            {
                "page": page,
            }
        )


class AssetCreateView(TemplateView):

    template_name = "crud/form.html"

    def get(self, request):

        
        return self.render_to_response(
            {
                "page": AssetPageService().create_page(),
            }
        )

    def post(self, request):

        form = AssetCreateForm(request.POST)

        if not form.is_valid():

            return self.render_to_response(
                {
                    "page": AssetPageService().create_page(form),
                }
            )

        dto = AssetCreateDTO(
            company=form.cleaned_data["company"],
            asset_model=form.cleaned_data["asset_model"],
            serial_number=form.cleaned_data["serial_number"],
            purchase_date=form.cleaned_data["purchase_date"],
            received_date=form.cleaned_data["received_date"],
            purchase_cost=form.cleaned_data["purchase_cost"],
            invoice_number=form.cleaned_data["invoice_number"],
            condition=form.cleaned_data["condition"],
            remarks=form.cleaned_data["remarks"],
        )

        AssetService().create(dto)

        messages.success(
            request,
            "Asset registered successfully.",
        )

        return redirect("assets:asset-list")


class AssetDetailView(TemplateView):

    template_name = "crud/form.html"

    def get(self, request, pk):

        asset = AssetRepository().get(pk)
        page = AssetPageService().detail_page(asset)

        return self.render_to_response(
            {
                "page": page,
            }
        )


class AssetUpdateView(TemplateView):

    template_name = "crud/form.html"

    def get(self, request, pk):

        asset = AssetRepository().get(pk)

        return self.render_to_response(
            {
                "page": AssetPageService().update_page(asset),
            }
        )

    def post(self, request, pk):

        asset = AssetRepository().get(pk)

        form = AssetUpdateForm(
            request.POST,
            instance=asset,
        )

        if not form.is_valid():

            return self.render_to_response(
                {
                    "page": AssetPageService().update_page(
                        asset,
                        form,
                    ),
                }
            )

        dto = AssetUpdateDTO(
            company=form.cleaned_data["company"],
            asset_model=form.cleaned_data["asset_model"],
            serial_number=form.cleaned_data["serial_number"],
            purchase_date=form.cleaned_data["purchase_date"],
            received_date=form.cleaned_data["received_date"],
            purchase_cost=form.cleaned_data["purchase_cost"],
            invoice_number=form.cleaned_data["invoice_number"],
            condition=form.cleaned_data["condition"],
            remarks=form.cleaned_data["remarks"],
            is_active=form.cleaned_data["is_active"],
        )

        AssetService().update(
            asset,
            dto,
        )

        messages.success(
            request,
            "Asset updated successfully.",
        )

        return redirect("assets:asset-list")


class AssetDeleteView(TemplateView):

    template_name = "common/delete.html"

    def post(self, request, pk):

        asset = AssetRepository().get(pk)

        AssetService().delete(asset)

        messages.success(
            request,
            "Asset deleted successfully.",
        )

        return redirect("assets:asset-list")