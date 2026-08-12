from django.contrib import messages
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.views import View

from core.permissions.mixins import PermissionRequiredMixin

from organizations.dtos import (
    JobTitleCreateDTO,
    JobTitleUpdateDTO,
)

from organizations.models import JobTitle

from organizations.page_services.job_title_page_service import (
    JobTitlePageService,
)

from organizations.services.job_title import (
    JobTitleService,
)


class JobTitleListView(PermissionRequiredMixin, View):

    page_service = JobTitlePageService()

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


class JobTitleCreateView(PermissionRequiredMixin, View):

    page_service = JobTitlePageService()

    service = JobTitleService()

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

        dto = JobTitleCreateDTO(
            country=request.POST.get("country"),
            department=request.POST.get("department"),
            name=request.POST.get("name", ""),
            description=request.POST.get("description", ""),
        )

        self.service.create_job_title(dto)

        messages.success(
            request,
            "Job title created successfully.",
        )

        return redirect(
            "organizations:job-title-list",
        )


class JobTitleDetailView(PermissionRequiredMixin, View):

    page_service = JobTitlePageService()

    def get(
        self,
        request,
        pk,
    ):

        job_title = get_object_or_404(
            JobTitle,
            pk=pk,
        )

        page = self.page_service.detail_page(
            job_title,
        )

        return render(
            request,
            "crud/detail.html",
            {
                "page": page,
            },
        )


class JobTitleUpdateView(PermissionRequiredMixin, View):

    page_service = JobTitlePageService()

    service = JobTitleService()

    def get(
        self,
        request,
        pk,
    ):

        job_title = get_object_or_404(
            JobTitle,
            pk=pk,
        )

        page = self.page_service.update_page(
            job_title,
        )

        return render(
            request,
            "crud/detail.html",
            {
                "page": page,
            },
        )

    def post(
        self,
        request,
        pk,
    ):

        job_title = get_object_or_404(
            JobTitle,
            pk=pk,
        )

        dto = JobTitleUpdateDTO(
            country=request.POST.get("country"),
            department=request.POST.get("department"),
            name=request.POST.get("name", ""),
            description=request.POST.get("description", ""),
            is_active=request.POST.get("is_active") == "on",
        )

        self.service.update_job_title(
            job_title,
            dto,
        )

        messages.success(
            request,
            "Job title updated successfully.",
        )

        return redirect(
            "organizations:job-title-list",
        )


class JobTitleDeleteView(PermissionRequiredMixin, View):

    service = JobTitleService()

    def post(
        self,
        request,
        pk,
    ):

        job_title = get_object_or_404(
            JobTitle,
            pk=pk,
        )

        self.service.delete(
            job_title,
        )

        messages.success(
            request,
            "Job title deleted successfully.",
        )

        return redirect(
            "organizations:job-title-list",
        )
