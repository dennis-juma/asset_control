from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from core.permissions.constants import Permissions
from core.permissions.mixins import PermissionRequiredMixin
from core.services.country_context import CountryContextService



from assets.dtos import (
    BrandCreateDTO,
    BrandUpdateDTO,
)

from assets.forms import (
    BrandCreateForm,
    BrandUpdateForm,
)
from assets.page_services.brand_page_service import BrandPageService

from assets.repositories import BrandRepository
from assets.services import BrandService


class BrandListView(
    PermissionRequiredMixin,
    TemplateView):

    permission_required = Permissions.ASSET_VIEW

    template_name = "crud/list.html"

    def get(self, request, *args, **kwargs):
    
        page = BrandPageService().list_page(
            query=request.GET.get("q", ""),
            page=request.GET.get("page", 1),
            country_context=CountryContextService.resolve_request(request),
        )

        return self.render_to_response({
            "page": page,
        })


class BrandCreateView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_CREATE

    template_name = "crud/form.html"

    def get(self, request):

        page = BrandPageService().create_page()

        return self.render_to_response(
            {
    "page": page,
})

    def post(self, request):

        form = BrandCreateForm(request.POST)

        if not form.is_valid():
            return self.render_to_response(
                {
                    "form": form,
                    "title": "Create Brand",
                }
            )

        dto = BrandCreateDTO(
            country=form.cleaned_data["country"],
            name=form.cleaned_data["name"],
            description=form.cleaned_data["description"],
        )

        BrandService().create(dto)

        messages.success(
            request,
            "Brand created successfully.",
        )

        return redirect("assets:brand-list")


class BrandDetailView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_VIEW
    

    template_name = "crud/form.html"

    def get(self, request, pk):

        brand = BrandRepository().get(pk=pk)

        page = BrandPageService().detail_page(brand)

        return self.render_to_response(
            {
                "page": page,
            }
        )


class BrandUpdateView(
    PermissionRequiredMixin,
    TemplateView):

    permission_required = Permissions.ASSET_UPDATE

    template_name = "crud/form.html"

    def get(self, request, pk):

        brand = BrandRepository().get(pk=pk)

        page = BrandPageService().update_page(brand)

        return self.render_to_response(
            {
                "page": page,
            }
        )

    def post(self, request, pk):

        brand = BrandRepository().get(pk=pk)

        form = BrandUpdateForm(
            request.POST,
            instance=brand,
        )

        if not form.is_valid():
            return self.render_to_response(
                {
                    "form": form,
                    "object": brand,
                }
            )

        dto = BrandUpdateDTO(
            country=form.cleaned_data["country"],
            
            name=form.cleaned_data["name"],
            description=form.cleaned_data["description"],
            
            is_active=form.cleaned_data["is_active"],
        )

        BrandService().update(
            brand,
            dto,
        )

        messages.success(
            request,
            "Brand updated successfully.",
        )

        return redirect("assets:brand-list")


class BrandDeleteView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_DELETE

    template_name = "crud/delete.html"

    def get(self, request, pk):

        brand = BrandRepository().get(pk=pk)

        return self.render_to_response(
            {
                "object": brand,
                "cancel_url": reverse("assets:brand-list"),
            }
        )

    def post(self, request, pk):

        brand = BrandRepository().get(pk=pk)

        try:
            BrandRepository().delete(brand)
        except ProtectedError:
            messages.error(
                request,
                "Brand cannot be deleted because it is in use.",
            )

            return redirect("assets:brand-list")

        messages.success(
            request,
            "Brand deleted successfully.",
        )

        return redirect("assets:brand-list")
