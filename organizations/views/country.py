from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.views import View

from core.permissions.mixins import PermissionRequiredMixin

from organizations.dtos import (
    CountryCreateDTO,
    CountryUpdateDTO,
)
from organizations.models import Country
from organizations.page_services.country_page_service import CountryPageService
from organizations.services import CountryService


class CountryListView(PermissionRequiredMixin, View):

    page_service = CountryPageService()

    def get(self, request):

        page = self.page_service.list_page(

            query=request.GET.get("q", ""),

            page=request.GET.get("page", 1),

        )

        return render(

            request,

            "crud/list.html",

            {

                "page": page,

            },

        )

class CountryCreateView(PermissionRequiredMixin, View):

    page_service = CountryPageService()

    service = CountryService()

    def get(self, request):

        page = self.page_service.create_page()

        return render(

            request,

            "crud/form.html",

            {

                "page": page,

            },

        )

    def post(self, request):

        dto = CountryCreateDTO(

            name=request.POST.get("name", ""),

            official_name=request.POST.get("official_name", ""),

            iso2=request.POST.get("iso2", ""),

            iso3=request.POST.get("iso3", ""),

            phone_code=request.POST.get("phone_code", ""),

            currency=request.POST.get("currency", ""),

            timezone=request.POST.get("timezone", ""),

            continent=request.POST.get("continent", ""),

            description=request.POST.get("description", ""),

        )

        self.service.create_country(dto)

        messages.success(

            request,

            "Country created successfully.",

        )

        return redirect(

            "organizations:country-list",

        )

class CountryDetailView(PermissionRequiredMixin, View):

    page_service = CountryPageService()

    def get(

        self,

        request,

        pk,

    ):

        country = get_object_or_404(

            Country,

            pk=pk,

        )

        page = self.page_service.detail_page(

            country,

        )

        return render(

            request,

            "crud/form.html",

            {

                "page": page,

            },

        )

class CountryUpdateView(PermissionRequiredMixin, View):

    page_service = CountryPageService()

    service = CountryService()

    def get(

        self,

        request,

        pk,

    ):

        country = get_object_or_404(

            Country,

            pk=pk,

        )

        page = self.page_service.update_page(

            country,

        )

        return render(

            request,

            "crud/form.html",

            {

                "page": page,

            },

        )

    def post(

        self,

        request,

        pk,

    ):

        country = get_object_or_404(

            Country,

            pk=pk,

        )

        dto = CountryUpdateDTO(

            name=request.POST.get("name", ""),

            official_name=request.POST.get("official_name", ""),

            iso2=request.POST.get("iso2", ""),

            iso3=request.POST.get("iso3", ""),

            phone_code=request.POST.get("phone_code", ""),

            currency=request.POST.get("currency", ""),

            timezone=request.POST.get("timezone", ""),

            continent=request.POST.get("continent", ""),

            description=request.POST.get("description", ""),

            is_active=request.POST.get("is_active") == "on",

        )

        self.service.update_country(

            country,

            dto,

        )

        messages.success(

            request,

            "Country updated successfully.",

        )

        return redirect(

            "organizations:country-list",

        )

class CountryDeleteView(PermissionRequiredMixin, View):

    service = CountryService()

    def post(

        self,

        request,

        pk,

    ):

        country = get_object_or_404(

            Country,

            pk=pk,

        )

        try:
            self.service.delete(country)
        except ProtectedError:
            messages.error(
                request,
                "Country cannot be deleted because it is in use.",
            )

            return redirect("organizations:country-list")

        messages.success(

            request,

            "Country deleted successfully.",

        )

        return redirect(

            "organizations:country-list",

        )
