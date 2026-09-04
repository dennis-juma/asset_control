from django.urls import reverse

from core.dtos import (
    BreadcrumbDTO,
    PageDTO,
)
from core.dtos.toolbar import (
    Toolbar,
    ToolbarButton,
)
from core.ui.datagrid.builder import DataGridBuilder
from core.ui.forms.builder import FormBuilder

from employees.forms import (
    EmployeeCreateForm,
    EmployeeUpdateForm,
)
from employees.repositories import EmployeeRepository


class EmployeePageService:

    def __init__(self):
        self.repository = EmployeeRepository()

    # =====================================================
    # List Page
    # =====================================================

    def list_page(
        self,
        query="",
        page=1,
        country_context=None,
    ) -> PageDTO:

        employees = self.repository.list(
            query=query,
            page=page,
            country_context=country_context,
        )

        grid = DataGridBuilder("Employees")
        grid.bulk_update("employees:employee-bulk-update", "employees")

        grid.column(
            field="employee_id",
            label="Employee ID",
        )

        grid.column(
            field="name",
            label="Name",
        )

        grid.column(
            field="country",
            label="Country",
        )

        grid.column(
            field="site",
            label="Site",
        )

        grid.column(
            field="department",
            label="Department",
        )

        grid.column(
            field="job_title",
            label="Job Title",
        )

        grid.column(
            field="manager",
            label="Manager",
        )

        grid.column(
            field="is_active",
            label="Status",
        )

        for employee in employees:

            grid.row(
                row_id=employee.pk,
                employee_id=employee.employee_id,
                name=employee.full_name,
                country=employee.country.name,
                site=employee.site.name,
                department=employee.department.name,
                job_title=employee.job_title.name,
                manager=employee.manager.full_name if employee.manager else "-",
                is_active=employee.is_active,
            )

        grid.action(
            title="View",
            icon="bi-eye",
            url_name="employees:employee-detail",
        )

        grid.action(
            title="Edit",
            icon="bi-pencil",
            url_name="employees:employee-update",
        )

        grid.action(
            title="Delete",
            icon="bi-trash",
            url_name="employees:employee-delete",
        )

        grid.paginate(employees)

        # Ensure the datagrid search form posts to the employee list route
        grid.search(
            reverse("employees:employee-list"),
            query=query,
            placeholder="Search employees...",
        )

        return PageDTO(
            title="Employees",
            subtitle="Manage employees",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Employees",
                ),
            ],
            toolbar=Toolbar(
    buttons=[
        ToolbarButton(
    label="Import",
    icon="bi-upload",
    url=reverse(
        "employees:employee-import",
    ),
    style="primary",
),
        ToolbarButton(
            label="Export",
            icon="bi-download",
            url=reverse(
                "employees:employee-export",
            ),
            style="secondary",
        ),

        ToolbarButton(
            label="New Employee",
            icon="bi-plus-lg",
            url=reverse(
                "employees:employee-create",
            ),
            style="warning",
        ),
    ],
),
            content=grid.build(),
        )

    # =====================================================
    # Create Page
    # =====================================================

    def create_page(self):

        form = EmployeeCreateForm()

        form_dto = (
            FormBuilder(
                title="Create Employee",
                form=form,
            )

            .section("Employee Information")

            .field("employee_id", width=4)
            .field("first_name", width=4)
            .field("middle_name", width=4)
            .field("last_name", width=4)
            .field("gender", width=4)

            .section("Organization")

            .field("country", width=6)
            .field("site", width=6)
            .field("department", width=6)
            .field("job_title", width=6)
            .field("manager", width=12)

            .section("Employment")

            .field("joining_date", width=6)
            .field("last_working_date", width=6)

            .section("Contact")

            .field("phone", width=6)
            .field("email", width=6)
            .field("photo", width=12)

            .section("Additional Information")

            .field("remarks", width=12)

            .submit(
                "Save",
                icon="save",
            )

            .reverse(
                "employees:employee-list",
            )

            .build()
        )

        return PageDTO(
            title="Create Employee",
            subtitle="Register a new employee",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Employees",
                    url=reverse(
                        "employees:employee-list",
                    ),
                ),
                BreadcrumbDTO(
                    label="Create",
                ),
            ],
            content=form_dto,
        )

    # =====================================================
    # Detail Page
    # =====================================================

    def detail_page(
        self,
        employee,
    ):

        form = EmployeeUpdateForm(
            instance=employee,
        )

        for field in form.fields.values():
            field.disabled = True

        form_dto = (
            FormBuilder(
                title="Employee Details",
                form=form,
            )

            .section("Employee Information")

            .field("employee_id", width=4)
            .field("first_name", width=4)
            .field("middle_name", width=4)
            .field("last_name", width=4)
            .field("gender", width=4)

            .section("Organization")

            .field("country", width=6)
            .field("site", width=6)
            .field("department", width=6)
            .field("job_title", width=6)
            .field("manager", width=12)

            .section("Employment")

            .field("joining_date", width=6)
            .field("last_working_date", width=6)

            .section("Contact")

            .field("phone", width=6)
            .field("email", width=6)
            .field("photo", width=12)

            .section("Additional Information")

            

                .field("system_role", width=6)
                .field("is_active", width=6)
                .field("remarks", width=12)

            .reverse(
                "employees:employee-list",
            )

            .build()
        )

        return PageDTO(
            title="Employee Details",
            subtitle=employee.full_name,
            breadcrumb=[
                BreadcrumbDTO(
                    label="Employees",
                    url=reverse(
                        "employees:employee-list",
                    ),
                ),
                BreadcrumbDTO(
                    label=employee.full_name,
                ),
            ],
            toolbar=Toolbar(
    buttons=[
        ToolbarButton(
            label="Export",
            icon="bi-download",
            url=reverse(
                "employees:employee-export",
            ),
            style="secondary",
        ),

        ToolbarButton(
            label="New Employee",
            icon="bi-plus-lg",
            url=reverse(
                "employees:employee-create",
            ),
            style="warning",
        ),
    ],
),
            content=form_dto,
        )

    # =====================================================
    # Update Page
    # =====================================================

    def update_page(
        self,
        employee,
    ):

        form = EmployeeUpdateForm(
            instance=employee,
        )

        form_dto = (
            FormBuilder(
                title="Edit Employee",
                form=form,
            )

            .section("Employee Information")

            .field("employee_id", width=4)
            .field("first_name", width=4)
            .field("middle_name", width=4)
            .field("last_name", width=4)
            .field("gender", width=4)

            .section("Organization")

            .field("country", width=6)
            .field("site", width=6)
            .field("department", width=6)
            .field("job_title", width=6)
            .field("manager", width=12)

            .section("Employment")

            .field("joining_date", width=6)
            .field("last_working_date", width=6)

            .section("Contact")

            .field("phone", width=6)
            .field("email", width=6)
            .field("photo", width=12)

            .section("Additional Information")
            .field("system_role", width=6)
            .field("is_active", width=12)
            .field("remarks", width=12)
            

            .submit(
                "Update",
                icon="save",
            )

            .reverse(
                "employees:employee-list",
            )

            .build()
        )

        return PageDTO(
            title="Edit Employee",
            subtitle=employee.full_name,
            breadcrumb=[
                BreadcrumbDTO(
                    label="Employees",
                    url=reverse(
                        "employees:employee-list",
                    ),
                ),
                BreadcrumbDTO(
                    label=employee.full_name,
                    url=reverse(
                        "employees:employee-detail",
                        args=[employee.pk],
                    ),
                ),
                BreadcrumbDTO(
                    label="Edit",
                ),
            ],
            content=form_dto,
        )
