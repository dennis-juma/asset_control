from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

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


class AssetCategoryListView(TemplateView):

    template_name = "crud/list.html"

    def get(self, request, *args, **kwargs):
    
        page = AssetCategoryPageService().list_page(
            query=request.GET.get("q", ""),
            page=request.GET.get("page", 1),
        )

        return self.render_to_response({
            "page": page,
        })


class AssetCategoryCreateView(TemplateView):

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
            company=form.cleaned_data["company"],
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


class AssetCategoryDetailView(TemplateView):

    template_name = "crud/form.html"

    def get(self, request, pk):

        category = AssetCategoryRepository().get(pk=pk)

        page = AssetCategoryPageService().detail_page(category)

        return self.render_to_response(
            {
                "page": page,
            }
        )


class AssetCategoryUpdateView(TemplateView):

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
            company=form.cleaned_data["company"],
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


class AssetCategoryDeleteView(TemplateView):

    template_name = "common/delete.html"

    def post(self, request, pk):

        category = AssetCategoryRepository().get(pk=pk)

        AssetCategoryRepository().delete(category)

        messages.success(
            request,
            "Asset Category deleted successfully.",
        )

        return redirect("assets:asset-category-list")