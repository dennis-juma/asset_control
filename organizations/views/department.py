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
    DepartmentCreateDTO,
    DepartmentUpdateDTO,
)
from organizations.models import Department
from organizations.page_services.department_page_service import (
    DepartmentPageService,
)
from organizations.services import DepartmentService


class DepartmentListView(PermissionRequiredMixin, View):

    page_service = DepartmentPageService()

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


class DepartmentCreateView(PermissionRequiredMixin, View):

    page_service = DepartmentPageService()
    service = DepartmentService()

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

        dto = DepartmentCreateDTO(
            country=request.POST.get("country"),
            site=request.POST.get("site"),
            parent=request.POST.get("parent") or None,
            name=request.POST.get("name"),
            cost_center=request.POST.get("cost_center", ""),
            description=request.POST.get("description", ""),
        )

        self.service.create_department(dto)

        messages.success(
            request,
            "Department created successfully.",
        )

        return redirect(
            "organizations:department-list",
        )


class DepartmentDetailView(PermissionRequiredMixin, View):

    page_service = DepartmentPageService()

    def get(
        self,
        request,
        pk,
    ):

        department = get_object_or_404(
            Department,
            pk=pk,
        )

        page = self.page_service.detail_page(
            department,
        )

        return render(
            request,
            "crud/form.html",
            {
                "page": page,
            },
        )


class DepartmentUpdateView(PermissionRequiredMixin, View):

    page_service = DepartmentPageService()
    service = DepartmentService()

    def get(
        self,
        request,
        pk,
    ):

        department = get_object_or_404(
            Department,
            pk=pk,
        )

        page = self.page_service.update_page(
            department,
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

        department = get_object_or_404(
            Department,
            pk=pk,
        )

        dto = DepartmentUpdateDTO(
            country=request.POST.get("country"),
            site=request.POST.get("site"),
            parent=request.POST.get("parent") or None,
            name=request.POST.get("name"),
            cost_center=request.POST.get("cost_center", ""),
            description=request.POST.get("description", ""),
            is_active=request.POST.get("is_active") == "on",
        )

        self.service.update_department(
            department,
            dto,
        )

        messages.success(
            request,
            "Department updated successfully.",
        )

        return redirect(
            "organizations:department-list",
        )


class DepartmentDeleteView(PermissionRequiredMixin, View):

    service = DepartmentService()

    def post(
        self,
        request,
        pk,
    ):

        department = get_object_or_404(
            Department,
            pk=pk,
        )

        try:
            self.service.delete(department)
        except ProtectedError:
            messages.error(
                request,
                "Department cannot be deleted because it is in use.",
            )

            return redirect("organizations:department-list")

        messages.success(
            request,
            "Department deleted successfully.",
        )

        return redirect(
            "organizations:department-list",
        )
