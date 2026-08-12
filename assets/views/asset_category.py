from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from core.permissions.constants import Permissions
from core.permissions.mixins import PermissionRequiredMixin

from assets.dtos import (
    AssetCategoryCreateDTO,
    AssetCategoryUpdateDTO,
)
from assets.forms.asset_category import (
    AssetCategoryCreateForm,
    AssetCategoryUpdateForm,
)
from assets.page_services import AssetCategoryPageService
from assets.repositories import AssetCategoryRepository
from assets.services import AssetCategoryService


class AssetCategoryListView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_VIEW

    template_name = "crud/list.html"

    def get(self, request, *args, **kwargs):
    
        page = AssetCategoryPageService().list_page(
            query=request.GET.get("q", ""),
            page=request.GET.get("page", 1),
        )

        return self.render_to_response({
            "page": page,
        })


class AssetCategoryCreateView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_CREATE

    template_name = "crud/form.html"

    def get(self, request):

        page = AssetCategoryPageService().create_page()

        return self.render_to_response(
            {
    "page": page,
})

    def post(self, request):

        form = AssetCategoryCreateForm(request.POST)

        if not form.is_valid():
            return self.render_to_response(
                {
                    "form": form,
                    "title": "Create Asset Category",
                }
            )

        dto = AssetCategoryCreateDTO(
            country=form.cleaned_data["country"],
            parent=form.cleaned_data["parent"],
            name=form.cleaned_data["name"],
            description=form.cleaned_data["description"],
            sort_order=form.cleaned_data["sort_order"],
        )

        AssetCategoryService().create(dto)

        messages.success(
            request,
            "Asset Category created successfully.",
        )

        return redirect("assets:asset-category-list")


class AssetCategoryDetailView(
     PermissionRequiredMixin,
    TemplateView):

    permission_required = Permissions.ASSET_VIEW

    template_name = "crud/form.html"

    def get(self, request, pk):

        category = AssetCategoryRepository().get(pk=pk)

        page = AssetCategoryPageService().detail_page(category)

        return self.render_to_response(
            {
                "page": page,
            }
        )


class AssetCategoryUpdateView(
     PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_UPDATE

    template_name = "crud/form.html"

    def get(self, request, pk):

        category = AssetCategoryRepository().get(pk=pk)

        page = AssetCategoryPageService().update_page(category)

        return self.render_to_response(
            {
                "page": page,
            }
        )

    def post(self, request, pk):

        category = AssetCategoryRepository().get(pk=pk)

        form = AssetCategoryUpdateForm(
            request.POST,
            instance=category,
        )

        if not form.is_valid():
            return self.render_to_response(
                {
                    "form": form,
                    "object": category,
                }
            )

        dto = AssetCategoryUpdateDTO(
            country=form.cleaned_data["country"],
            parent=form.cleaned_data["parent"],
            name=form.cleaned_data["name"],
            description=form.cleaned_data["description"],
            sort_order=form.cleaned_data["sort_order"],
            is_active=form.cleaned_data["is_active"],
        )

        AssetCategoryService().update(
            category,
            dto,
        )

        messages.success(
            request,
            "Asset Category updated successfully.",
        )

        return redirect("assets:asset-category-list")


class AssetCategoryDeleteView(
     PermissionRequiredMixin,
    TemplateView):

    permission_required = Permissions.ASSET_DELETE

    template_name = "crud/delete.html"

    def get(self, request, pk):

        category = AssetCategoryRepository().get(pk=pk)

        return self.render_to_response(
            {
                "object": category,
                "cancel_url": reverse("assets:asset-category-list"),
            }
        )

    def post(self, request, pk):

        category = AssetCategoryRepository().get(pk=pk)

        try:
            AssetCategoryRepository().delete(category)
        except ProtectedError:
            messages.error(
                request,
                "Asset Category cannot be deleted because it is in use.",
            )

            return redirect("assets:asset-category-list")

        messages.success(
            request,
            "Asset Category deleted successfully.",
        )

        return redirect("assets:asset-category-list")
