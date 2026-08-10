from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.views import View

from employees.dtos import (
    EmployeeCreateDTO,
    EmployeeUpdateDTO,
)
from employees.models import Employee
from employees.page_services import EmployeePageService
from employees.services import EmployeeService
from organizations.models import (
    Company,
    Department,
    JobTitle,
    Site,
)

User = get_user_model()


class EmployeeListView(View):

    page_service = EmployeePageService()

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


class EmployeeCreateView(View):

    page_service = EmployeePageService()
    service = EmployeeService()

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

        manager_id = request.POST.get("manager") or None
        user_id = request.POST.get("user") or None

        dto = EmployeeCreateDTO(

            company=get_object_or_404(
                Company,
                pk=request.POST.get("company"),
            ),

            site=get_object_or_404(
                Site,
                pk=request.POST.get("site"),
            ),

            department=get_object_or_404(
                Department,
                pk=request.POST.get("department"),
            ),

            job_title=get_object_or_404(
                JobTitle,
                pk=request.POST.get("job_title"),
            ),

            manager=(
                get_object_or_404(Employee, pk=manager_id)
                if manager_id
                else None
            ),

            user=(
                get_object_or_404(User, pk=user_id)
                if user_id
                else None
            ),

            employee_id=request.POST.get("employee_id", ""),

            first_name=request.POST.get("first_name", ""),

            middle_name=request.POST.get("middle_name", ""),

            last_name=request.POST.get("last_name", ""),

            gender=request.POST.get("gender", ""),

            joining_date=request.POST.get("joining_date"),

            last_working_date=request.POST.get("last_working_date") or None,

            phone=request.POST.get("phone", ""),

            email=request.POST.get("email", ""),

            photo=request.FILES.get("photo"),

            remarks=request.POST.get("remarks", ""),
        )

        self.service.create_employee(dto)

        messages.success(
            request,
            "Employee created successfully.",
        )

        return redirect(
            "employees:employee-list",
        )


class EmployeeDetailView(View):

    page_service = EmployeePageService()

    def get(
        self,
        request,
        pk,
    ):

        employee = get_object_or_404(
            Employee,
            pk=pk,
        )

        page = self.page_service.detail_page(
            employee,
        )

        return render(
            request,
            "crud/form.html",
            {
                "page": page,
            },
        )


class EmployeeUpdateView(View):

    page_service = EmployeePageService()
    service = EmployeeService()

    def get(
        self,
        request,
        pk,
    ):

        employee = get_object_or_404(
            Employee,
            pk=pk,
        )

        page = self.page_service.update_page(
            employee,
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

        employee = get_object_or_404(
            Employee,
            pk=pk,
        )

        manager_id = request.POST.get("manager") or None
        user_id = request.POST.get("user") or None

        dto = EmployeeUpdateDTO(

            company=get_object_or_404(
                Company,
                pk=request.POST.get("company"),
            ),

            site=get_object_or_404(
                Site,
                pk=request.POST.get("site"),
            ),

            department=get_object_or_404(
                Department,
                pk=request.POST.get("department"),
            ),

            job_title=get_object_or_404(
                JobTitle,
                pk=request.POST.get("job_title"),
            ),

            manager=(
                get_object_or_404(Employee, pk=manager_id)
                if manager_id
                else None
            ),

            user=(
                get_object_or_404(User, pk=user_id)
                if user_id
                else None
            ),

            employee_id=request.POST.get("employee_id", ""),

            first_name=request.POST.get("first_name", ""),

            middle_name=request.POST.get("middle_name", ""),

            last_name=request.POST.get("last_name", ""),

            gender=request.POST.get("gender", ""),

            joining_date=request.POST.get("joining_date"),

            last_working_date=request.POST.get("last_working_date") or None,

            phone=request.POST.get("phone", ""),

            email=request.POST.get("email", ""),

            photo=request.FILES.get("photo"),

            remarks=request.POST.get("remarks", ""),

            is_active=request.POST.get("is_active") == "on",
        )

        self.service.update_employee(
            employee,
            dto,
        )

        messages.success(
            request,
            "Employee updated successfully.",
        )

        return redirect(
            "employees:employee-list",
        )


class EmployeeDeleteView(View):

    service = EmployeeService()

    def post(
        self,
        request,
        pk,
    ):

        employee = get_object_or_404(
            Employee,
            pk=pk,
        )

        self.service.delete(
            employee,
        )

        messages.success(
            request,
            "Employee deleted successfully.",
        )

        return redirect(
            "employees:employee-list",
        )