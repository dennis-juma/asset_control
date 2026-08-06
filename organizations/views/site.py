from django.contrib import messages
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.views import View

from organizations.dtos import (
    SiteCreateDTO,
    SiteUpdateDTO,
)
from organizations.models import Site
from organizations.page_services.site_page_service import SitePageService
from organizations.services import SiteService



class SiteListView(View):

    page_service = SitePageService()

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

class SiteCreateView(View):

    page_service = SitePageService()

    service = SiteService()

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

        dto = SiteCreateDTO(

            company_id=request.POST.get("company"),

            country_id=request.POST.get("country"),

            name=request.POST.get("name"),

            site_type=request.POST.get("site_type"),

            email=request.POST.get("email", ""),

            phone=request.POST.get("phone", ""),

            address=request.POST.get("address", ""),

            city=request.POST.get("city", ""),

            postal_code=request.POST.get("postal_code", ""),

            latitude=request.POST.get("latitude") or None,

            longitude=request.POST.get("longitude") or None,


        )

        self.service.create_site(dto)

        messages.success(

            request,

            "Site created successfully.",

        )

        return redirect(

            "organizations:site-list",

        )

class SiteDetailView(View):

    page_service = SitePageService()

    def get(

        self,

        request,

        pk,

    ):

        site = get_object_or_404(

            Site,

            pk=pk,

        )

        page = self.page_service.detail_page(

            site,

        )

        return render(

            request,

            "crud/form.html",

            {

                "page": page,

            },

        )

class SiteUpdateView(View):

    page_service = SitePageService()

    service = SiteService()

    def get(

        self,

        request,

        pk,

    ):

        site = get_object_or_404(

            Site,

            pk=pk,

        )

        page = self.page_service.update_page(

            site,

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

        site = get_object_or_404(

            Site,

            pk=pk,

        )

        dto = SiteUpdateDTO(

            company_id=request.POST.get("company"),

            country_id=request.POST.get("country"),

            name=request.POST.get("name"),

            site_type=request.POST.get("site_type"),

            email=request.POST.get("email", ""),

            phone=request.POST.get("phone", ""),

            address=request.POST.get("address", ""),

            city=request.POST.get("city", ""),

            postal_code=request.POST.get("postal_code", ""),

            latitude=request.POST.get("latitude") or None,

            longitude=request.POST.get("longitude") or None,

            is_active=request.POST.get("is_active") == "on",

        )

        self.service.update_site(

            site,

            dto,

        )

        messages.success(

            request,

            "Site updated successfully.",

        )

        return redirect(

            "organizations:site-list",

        )


class SiteDeleteView(View):

    service = SiteService()

    def post(

        self,

        request,

        pk,

    ):

        site = get_object_or_404(

            Site,

            pk=pk,

        )

        self.service.delete(

            site,

        )

        messages.success(

            request,

            "Site deleted successfully.",

        )

        return redirect(

            "organizations:site-list",

        )