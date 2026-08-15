from django.contrib import messages
from django.db.models.deletion import ProtectedError
from core.permissions.constants import Permissions
from core.permissions.mixins import PermissionRequiredMixin
from core.services.country_context import CountryContextService
from core.views.bulk_status import BulkStatusUpdateView
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from core.dtos.export import ExportRequestDTO
from core.exports.enums import ExportType
from core.exports.service import ExportService

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
from assets.models import Asset


class AssetBulkUpdateView(PermissionRequiredMixin, BulkStatusUpdateView):
    permission_required = Permissions.ASSET_UPDATE
    model = Asset
    redirect_url = "assets:asset-list"
    record_label = "asset"


class AssetListView(
     PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_VIEW

    template_name = "crud/list.html"

    def get(self, request, *args, **kwargs):

        page = AssetPageService().list_page(
            query=request.GET.get("q", ""),
            page=request.GET.get("page", 1),
            country_context=CountryContextService.resolve_request(request),
        )

        return self.render_to_response(
            {
                "page": page,
            }
        )


class AssetExportView(PermissionRequiredMixin, TemplateView):
    permission_required = Permissions.ASSET_EXPORT

    def get(self, request, *args, **kwargs):
        export_type = request.GET.get("format", "xlsx")

        if export_type not in ("csv", "xlsx"):
            messages.error(
                request,
                "Unsupported export format.",
            )
            return redirect("assets:asset-list")

        query = request.GET.get("q", "").strip()

        queryset = AssetRepository().export_queryset(
            query=query,
            country_context=CountryContextService.resolve_request(request),
        )

        from core.ui.datagrid import DataGridBuilder

        grid = DataGridBuilder(
            title="Assets"
        )

        grid.column(
            field="asset_tag",
            label="Asset Tag",
        )
        grid.column(
            field="serial_number",
            label="Serial Number",
        )
        grid.column(
            field="country",
            label="Country",
        )
        grid.column(
            field="category",
            label="Category",
        )
        grid.column(
            field="brand",
            label="Brand",
        )
        grid.column(
            field="model",
            label="Model",
        )
        grid.column(
            field="status",
            label="Status",
        )
        grid.column(
            field="condition",
            label="Condition",
        )
        grid.column(
            field="purchase_date",
            label="Purchase Date",
        )
        grid.column(
            field="purchase_cost",
            label="Purchase Cost",
        )

        for asset in queryset:
            grid.row(
                asset.id,
                asset_tag=asset.asset_tag,
                serial_number=asset.serial_number,
                country=(
                    asset.country.name
                    if asset.country
                    else ""
                ),
                category=(
                    asset.asset_model.category.name
                    if asset.asset_model
                    and asset.asset_model.category
                    else ""
                ),
                brand=(
                    asset.asset_model.brand.name
                    if asset.asset_model
                    and asset.asset_model.brand
                    else ""
                ),
                model=(
                    asset.asset_model.name
                    if asset.asset_model
                    else ""
                ),
                status=asset.get_status_display(),
                condition=asset.get_condition_display(),
                purchase_date=asset.purchase_date or "",
                purchase_cost=asset.purchase_cost or "",
            )

        from core.dtos.export import ExportRequestDTO
        from core.exports.enums import ExportType
        from core.exports.service import ExportService

        export_request = ExportRequestDTO(
            filename="assets",
            title="Assets",
            export_type=ExportType(export_type),
        )

        return ExportService.export(
            grid.build(),
            export_request,
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
