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

from organizations.forms import (
    DepartmentCreateForm,
    DepartmentUpdateForm,
)
from organizations.repositories import DepartmentRepository
from organizations.services import DepartmentService


class DepartmentPageService:

    def __init__(self):

        self.service = DepartmentService()

        self.repository = DepartmentRepository()

    # --------------------------------------------------
    # LIST
    # --------------------------------------------------

    def list_page(
        self,
        query="",
        page=1,
    ) -> PageDTO:

        departments = self.repository.list(
            query=query,
            page=page,
        )

        grid = DataGridBuilder("Departments")

        grid.column(
            field="code",
            label="Code",
        )

        grid.column(
            field="name",
            label="Department",
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
            field="parent",
            label="Parent",
        )

        grid.column(
            field="cost_center",
            label="Cost Center",
        )

        grid.column(
            field="is_active",
            label="Status",
        )

        for department in departments:

            grid.row(
                row_id=department.id,
                code=department.code,
                name=department.name,
                country=department.country.name,
                parent=department.parent.name if department.parent else "-",
                cost_center=department.cost_center,
                is_active=department.is_active,
            )

        grid.action(
            title="View",
            icon="bi-eye",
            url_name="organizations:department-detail",
        )

        grid.action(
            title="Edit",
            icon="bi-pencil",
            url_name="organizations:department-update",
        )

        grid.action(
            title="Delete",
            icon="bi-trash",
            url_name="organizations:department-delete",
        )

        grid.paginate(departments)

        return PageDTO(
            title="Departments",
            subtitle="Manage departments",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Organizations",
                    url="/organizations/",
                ),
                BreadcrumbDTO(
                    label="Departments",
                ),
            ],
            toolbar=Toolbar(
                buttons=[
                    ToolbarButton(
                        label="New Department",
                        icon="bi-plus-lg",
                        url=reverse(
                            "organizations:department-create",
                        ),
                        style="warning",
                    ),
                ],
            ),
            content=grid.build(),
        )

    # --------------------------------------------------
    # CREATE
    # --------------------------------------------------

    def create_page(self):

        form = DepartmentCreateForm()

        form_dto = (
            FormBuilder(
                title="Create Department",
                form=form,
            )

            .section("General Information")

            .field("country", width=6)
            .field("parent", width=6)
            .field("name", width=6)

            .section("Organization")

            .field("cost_center", width=6)

            .section("Additional Information")

            .field("description", width=12)

            .submit(
                "Save",
                icon="save",
            )

            .reverse(
                "organizations:department-list",
            )

            .build()
        )

        return PageDTO(
            title="Create Department",
            subtitle="Register a new department",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Organizations",
                    url="/organizations/",
                ),
                BreadcrumbDTO(
                    label="Departments",
                    url=reverse(
                        "organizations:department-list",
                    ),
                ),
                BreadcrumbDTO(
                    label="Create",
                ),
            ],
            content=form_dto,
        )

    # --------------------------------------------------
    # DETAIL
    # --------------------------------------------------

    def detail_page(
        self,
        department,
    ):

        form = DepartmentUpdateForm(
            instance=department,
        )

        for field in form.fields.values():
            field.disabled = True

        form_dto = (
            FormBuilder(
                title="Department Details",
                form=form,
            )

            .section("General Information")

            .field("country", 6)
            .field("parent", 6)
            .field("name", 6)

            .section("Organization")

            .field("cost_center", 6)
            

            .section("Additional Information")

            .field("description", 12)

            .reverse(
                "organizations:department-list",
            )

            .build()
        )

        return PageDTO(
            title="Department Details",
            subtitle=department.name,
            breadcrumb=[
                BreadcrumbDTO(
                    label="Organizations",
                    url="/organizations/",
                ),
                BreadcrumbDTO(
                    label="Departments",
                    url=reverse(
                        "organizations:department-list",
                    ),
                ),
                BreadcrumbDTO(
                    label=department.name,
                ),
            ],
            toolbar=Toolbar(
                buttons=[
                    ToolbarButton(
                        label="Edit",
                        icon="bi-pencil",
                        url=reverse(
                            "organizations:department-update",
                            kwargs={
                                "pk": department.id,
                            },
                        ),
                        style="warning",
                    ),
                    ToolbarButton(
                        label="Back",
                        icon="bi-arrow-left",
                        url=reverse(
                            "organizations:department-list",
                        ),
                        style="secondary",
                    ),
                ],
            ),
            content=form_dto,
        )

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    def update_page(
        self,
        department,
    ):

        form = DepartmentUpdateForm(
            instance=department,
        )

        form_dto = (
            FormBuilder(
                title="Edit Department",
                form=form,
            )

            .section("General Information")

            .field("country", 6)
            .field("parent", 6)
            .field("name", 6)

            .section("Organization")

            .field("cost_center", 6)
            
            .section("Additional Information")

            .field("description", 12)

            .section("Status")

            .field("is_active", 12)

            .submit(
                "Update",
                icon="save",
            )

            .reverse(
                "organizations:department-list",
            )

            .build()
        )

        return PageDTO(
            title="Edit Department",
            subtitle=department.name,
            breadcrumb=[
                BreadcrumbDTO(
                    label="Organizations",
                    url="/organizations/",
                ),
                BreadcrumbDTO(
                    label="Departments",
                    url=reverse(
                        "organizations:department-list",
                    ),
                ),
                BreadcrumbDTO(
                    label=department.name,
                    url=reverse(
                        "organizations:department-detail",
                        args=[department.pk],
                    ),
                ),
                BreadcrumbDTO(
                    label="Edit",
                ),
            ],
            content=form_dto,
        )