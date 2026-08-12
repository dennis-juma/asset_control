from django.contrib import messages
from django.db.models.deletion import ProtectedError
from core.permissions.constants import Permissions
from core.permissions.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
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


class AssetListView(
     PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_VIEW

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


class AssetCreateView(
     PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_CREATE

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
            country=form.cleaned_data["country"],
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


class AssetDetailView(
     PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_VIEW

    template_name = "crud/form.html"

    def get(self, request, pk):

        asset = AssetRepository().get(pk)
        page = AssetPageService().detail_page(asset)

        return self.render_to_response(
            {
                "page": page,
            }
        )


class AssetUpdateView(
     PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_UPDATE

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
            country=form.cleaned_data["country"],
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


class AssetDeleteView(
     PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_DELETE

    template_name = "crud/delete.html"

    def get(self, request, pk):

        asset = AssetRepository().get(pk)

        return self.render_to_response(
            {
                "object": asset,
                "cancel_url": reverse("assets:asset-list"),
            }
        )

    def post(self, request, pk):

        asset = AssetRepository().get(pk)

        try:
            AssetService().delete(asset)
        except ProtectedError:
            messages.error(
                request,
                "Asset cannot be deleted because it is in use.",
            )

            return redirect("assets:asset-list")

        messages.success(
            request,
            "Asset deleted successfully.",
        )

        return redirect("assets:asset-list")
