from urllib import request

from django.contrib import messages
from django.db.models import query
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from organizations.forms import (
    CompanyCreateForm,
    CompanyUpdateForm,
)
from organizations.dtos import CompanyCreateDTO, CompanyUpdateDTO
from organizations.models import Company
from organizations.page_services import CompanyPageService
from organizations.services import CompanyService


class CompanyListView(View):

    page_service = CompanyPageService()



    def get(self, request):

        query = request.GET.get("q", "").strip()
        page_number = request.GET.get("page", 1)

        page = self.page_service.list_page(
            query=query,
            page=page_number,
        )

        return render(
            request,
            "crud/list.html",
            {
                "page": page,
            },
        )


class CompanyCreateView(View):

    page_service = CompanyPageService()
    service = CompanyService()

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

        form = CompanyCreateForm(request.POST, request.FILES)

        if form.is_valid():

            self.service.create_company(
                CompanyCreateDTO(**form.cleaned_data)
            )

            messages.success(
                request,
                "Company created successfully.",
            )

            return redirect("organizations:company-list")

        page = self.page_service.create_page(form)

        return render(
            request,
            "crud/form.html",
            {
                "page": page,
            },
        )


class CompanyUpdateView(View):

    page_service = CompanyPageService()
    service = CompanyService()

    def get(self, request, pk):

        company = get_object_or_404(
            Company,
            pk=pk,
        )

        page = self.page_service.edit_page(company)

        return render(
            request,
            "crud/form.html",
            {
                "page": page,
            },
        )

    def post(self, request, pk):

        company = get_object_or_404(
            Company,
            pk=pk,
        )

        form = CompanyUpdateForm(
            request.POST,
            request.FILES,
            instance=company,
        )

        if form.is_valid():

            self.service.update_company(
                company,
                CompanyUpdateDTO(**form.cleaned_data),
            )

            messages.success(
                request,
                "Company updated successfully.",
            )

            return redirect("organizations:company-list")

        page = self.page_service.edit_page(
            company,
            form,
        )

        return render(
            request,
            "crud/form.html",
            {
                "page": page,
            },
        )


class CompanyDetailView(View):
    def get(self, request, pk):

        company = get_object_or_404(
            Company,
            pk=pk,
        )

        return render(
            request,
            "crud/detail.html",
            {
                "company": company,
            },
        )


class CompanyDeleteView(View):
    service = CompanyService()

    def post(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        self.service.delete(company)
        messages.success(request, "Company deleted successfully.")
        return redirect("organizations:company-list")
