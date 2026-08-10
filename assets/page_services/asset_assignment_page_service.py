from django.urls import reverse
from assets.forms import (
    AssetAssignmentCreateForm,
    AssetReturnForm,
    AssetAssignmentUpdateForm,
    
)
from assets.repositories import AssetAssignmentRepository
from assets.choices.choices import AssignmentStatus,AssignmentType
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


# =====================================================
# List Page
# =====================================================
class AssetAssignmentPageService:

    def __init__(self):
        self.repository = AssetAssignmentRepository()

    def list_page(
        self,
        query="",
        page=1,
    ) -> PageDTO:

        assignments = self.repository.list(
            query=query,
            page=page,
        )

        grid = DataGridBuilder("Asset Assignments")

        grid.column(
            field="asset",
            label="Asset",
        )

        grid.column(
            field="assigned_to",
            label="Assigned To",
        )

        grid.column(
            field="assigned_date",
            label="Assigned Date",
        )

        grid.column(
            field="expected_return_date",
            label="Expected Return",
        )

        grid.column(
            field="status",
            label="Status",
        )

        for assignment in assignments:

            assigned_to = (
                assignment.employee.full_name
                if assignment.employee
                else assignment.site.name
            )

            grid.row(
                row_id=assignment.pk,
                asset=assignment.asset.asset_tag,
                assigned_to=assigned_to,
                assigned_date=assignment.assigned_date,
                expected_return_date=assignment.expected_return_date or "-",
                status=assignment.get_status_display(),
            )

        grid.action(
            title="View",
            icon="bi-eye",
            url_name="assets:asset-assignment-detail",
        )

        grid.action(
            title="Edit",
            icon="bi-pencil",
            url_name="assets:asset-assignment-update",
        )

        grid.action(
            title="Return",
            icon="bi-arrow-return-left",
            url_name="assets:asset-return",
        )

        grid.paginate(assignments)

        return PageDTO(
            title="Asset Assignments",
            subtitle="Manage Asset Assignments",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Assignments",
                ),
            ],
            toolbar=Toolbar(
                buttons=[
                    ToolbarButton(
                        label="Assign Asset",
                        icon="bi-plus-lg",
                        url=reverse(
                            "assets:asset-assignment-create",
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

    def create_page(
        self,
        form=None,
    ):

        if form is None:
            form = AssetAssignmentCreateForm()

        form_dto = (
            FormBuilder(
                title="Assign Asset",
                form=form,
            )

            .section("Assignment Information")

            .field("company", width=6)
            .field("asset", width=6)

            .field("assignment_type", width=12)

            .field("employee", width=6)
            .field("site", width=6)

            .section("Assignment Dates")

            .field("assigned_date", width=6)
            .field("expected_return_date", width=6)

            .section("Remarks")

            .field("remarks", width=12)

            .submit(
                "Assign Asset",
                icon="save",
            )

            .reverse(
                "assets:asset-assignment-list",
            )

            .build()
        )

        return PageDTO(
            title="Assign Asset",
            subtitle="Assign an Asset to an Employee or Site",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Assignments",
                    url=reverse(
                        "assets:asset-assignment-list",
                    ),
                ),
                BreadcrumbDTO(
                    label="Assign Asset",
                ),
            ],
            content=form_dto,
        )


    # =====================================================
    # Detail Page
    # =====================================================

    def detail_page(
        self,
        assignment,
    ):

        form = AssetAssignmentUpdateForm(
            instance=assignment,
        )

        # Make every field read-only
        for field in form.fields.values():
            field.disabled = True

        form_dto = (
            FormBuilder(
                title="Assignment Details",
                form=form,
            )

            .section("Assignment Information")
            .field("assignment_type", width=12)
            .field("employee", width=6)
            .field("site", width=6)

            .section("Assignment Dates")

            .field("assigned_date", width=4)
            .field("expected_return_date", width=4)

            .section("Remarks")

            .field("remarks", width=12)

            .section("System")

            .field("is_active", width=12)

            .reverse(
                "assets:asset-assignment-list",
            )

            .build()
        )

        buttons = []

        if assignment.status == AssignmentStatus.ACTIVE:
            buttons.append(
                ToolbarButton(
                    label="Return Asset",
                    icon="bi-arrow-return-left",
                    url=reverse(
                        "assets:asset-return",
                        kwargs={
                            "pk": assignment.pk,
                        },
                    ),
                    style="warning",
                )
            )

        buttons.extend(
            [
                ToolbarButton(
                    label="Edit",
                    icon="bi-pencil",
                    url=reverse(
                        "assets:asset-assignment-update",
                        kwargs={
                            "pk": assignment.pk,
                        },
                    ),
                    style="primary",
                ),
                ToolbarButton(
                    label="Back",
                    icon="bi-arrow-left",
                    url=reverse(
                        "assets:asset-assignment-list",
                    ),
                    style="secondary",
                ),
            ]
        )

        return PageDTO(
            title="Assignment Details",
            subtitle=f"{assignment.asset.asset_tag}",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Assignments",
                    url=reverse(
                        "assets:asset-assignment-list",
                    ),
                ),
                BreadcrumbDTO(
                    label=assignment.asset.asset_tag,
                ),
            ],
            toolbar=Toolbar(
                buttons=buttons,
            ),
            content=form_dto,
        )

    

# =====================================================
# Return Page
# =====================================================

    def return_page(
        self,
        assignment,
        form=None,
    ):

        if form is None:
            form = AssetReturnForm()

        form_dto = (
            FormBuilder(
                title="Return Asset",
                form=form,
            )

            .section("Return Information")

            .field("returned_date", width=6)

            .field("remarks", width=12)

            .submit(
                "Return Asset",
                icon="arrow-return-left",
            )

            .reverse(
                "assets:asset-assignment-detail",
                kwargs={
                    "pk": assignment.pk,
                },
            )

            .build()
        )

        assigned_to = (
            assignment.employee.full_name
            if assignment.employee
            else assignment.site.name
        )

        return PageDTO(
            title="Return Asset",

            subtitle=assignment.asset.asset_tag,

            description=[
                assignment.asset.asset_model.name,
                f"Assigned To: {assigned_to}",
                f"Assigned Date: {assignment.assigned_date}",
                f"Status: {assignment.get_status_display()}",
            ],

            breadcrumb=[
                BreadcrumbDTO(
                    label="Assignments",
                    url=reverse(
                        "assets:asset-assignment-list",
                    ),
                ),
                BreadcrumbDTO(
                    label=assignment.asset.asset_tag,
                    url=reverse(
                        "assets:asset-assignment-detail",
                        kwargs={
                            "pk": assignment.pk,
                        },
                    ),
                ),
                BreadcrumbDTO(
                    label="Return",
                ),
            ],

            content=form_dto,
        )