from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView

from core.permissions.constants import Permissions
from core.permissions.mixins import PermissionRequiredMixin

from assets.dtos import (
    AssetModelCreateDTO,
    AssetModelUpdateDTO,
)
from assets.forms import (
    AssetModelCreateForm,
    AssetModelUpdateForm,
)
from assets.page_services import AssetModelPageService
from assets.repositories import AssetModelRepository
from assets.services import AssetModelService


class AssetModelListView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_VIEW

    template_name = "crud/list.html"

    def get(self, request, *args, **kwargs):

        page = AssetModelPageService().list_page(
            query=request.GET.get("q", ""),
            page=request.GET.get("page", 1),
        )

        return self.render_to_response(
            {
                "page": page,
            }
        )


class AssetModelCreateView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_CREATE

    template_name = "crud/form.html"

    def get(self, request):

        page = AssetModelPageService().create_page()

        return self.render_to_response(
            {
                "page": page,
            }
        )

    def post(self, request):

        form = AssetModelCreateForm(request.POST)

        if not form.is_valid():
            print(form.errors)

            return self.render_to_response(
                {
                    "page": AssetModelPageService().create_page(form),
                }
            )

        dto = AssetModelCreateDTO(
            company=form.cleaned_data["company"],
            category=form.cleaned_data["category"],
            brand=form.cleaned_data["brand"],
            name=form.cleaned_data["name"],
            manufacturer_part_number=form.cleaned_data["manufacturer_part_number"],
            technical_specifications=form.cleaned_data["technical_specifications"],
            description=form.cleaned_data["description"],
        )

        AssetModelService().create(dto)

        messages.success(
            request,
            "Asset Model created successfully.",
        )

        return redirect("assets:asset-model-list")


class AssetModelDetailView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_VIEW

    template_name = "crud/form.html"

    def get(self, request, pk):

        asset_model = AssetModelRepository().get(pk)

        page = AssetModelPageService().detail_page(asset_model)

        return self.render_to_response(
            {
                "page": page,
                }
        )


class AssetModelUpdateView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_UPDATE

    template_name = "crud/form.html"

    def get(self, request, pk):

        asset_model = AssetModelRepository().get(pk)

        page = AssetModelPageService().update_page(asset_model)

        return self.render_to_response(
            {
                "page": page,
            }
        )

    def post(self, request, pk):

        asset_model = AssetModelRepository().get(pk)

        form = AssetModelUpdateForm(
            request.POST,
            instance=asset_model,
        )

        if not form.is_valid():

            return self.render_to_response(
                {
                    "page": AssetModelPageService().update_page(
                        asset_model,
                        form,
                    ),
                }
            )

        dto = AssetModelUpdateDTO(
            company=form.cleaned_data["company"],
            category=form.cleaned_data["category"],
            brand=form.cleaned_data["brand"],
            name=form.cleaned_data["name"],
            manufacturer_part_number=form.cleaned_data["manufacturer_part_number"],
            technical_specifications=form.cleaned_data["technical_specifications"],
            description=form.cleaned_data["description"],
            is_active=form.cleaned_data["is_active"],
        )

        AssetModelService().update(
            asset_model,
            dto,
        )

        messages.success(
            request,
            "Asset Model updated successfully.",
        )

        return redirect("assets:asset-model-list")


class AssetModelDeleteView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_DELETE

    template_name = "common/delete.html"

    def post(self, request, pk):

        asset_model = AssetModelRepository().get(pk)

        AssetModelService().delete(asset_model)

        messages.success(
            request,
            "Asset Model deleted successfully.",
        )

        return redirect("assets:asset-model-list")