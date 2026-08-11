from django.urls import reverse

from assets.forms import (
    AssetCreateForm,
    AssetUpdateForm,
    AssetReturnForm,
    AssetAssignmentUpdateForm
    
)
from assets.repositories import AssetRepository
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


class AssetPageService:

    def __init__(self):
        self.repository = AssetRepository()

    # =====================================================
    # List Page
    # =====================================================

    def list_page(
        self,
        query="",
        page=1,
    ):

        assets = self.repository.list(
            query=query,
            page=page,
        )

        grid = DataGridBuilder("Assets")

        grid.column(
            field="asset_tag",
            label="Asset Tag",
        )

        grid.column(
            field="serial_number",
            label="Serial Number",
        )

        grid.column(
            field="asset_model",
            label="Model",
        )

        grid.column(
            field="company",
            label="Company",
        )

        grid.column(
            field="status",
            label="Status",
        )

        grid.column(
            field="condition",
            label="Condition",
        )

        for asset in assets:

            grid.row(
                row_id=asset.pk,
                asset_tag=asset.asset_tag,
                serial_number=asset.serial_number,
                asset_model=asset.asset_model.name,
                company=asset.company.name,
                status=asset.get_status_display(),
                condition=asset.get_condition_display(),
            )

        grid.action(
            title="View",
            icon="bi-eye",
            url_name="assets:asset-detail",
        )

        grid.action(
            title="Edit",
            icon="bi-pencil",
            url_name="assets:asset-update",
        )

        grid.action(
            title="Delete",
            icon="bi-trash",
            url_name="assets:asset-delete",
        )

        grid.paginate(assets)

        return PageDTO(
            title="Assets",
            subtitle="Manage Company Assets",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Assets",
                ),
            ],
            toolbar=Toolbar(
                buttons=[
                    ToolbarButton(
                        label="Register Asset",
                        icon="bi-plus-lg",
                        url=reverse(
                            "assets:asset-create",
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
            form = AssetCreateForm()

        form_dto = (
            FormBuilder(
                title="Register Asset",
                form=form,
            )

            .section("Asset Information")

            .field("company", width=6)
            .field("asset_model", width=6)

            .field("serial_number", width=12)

            .section("Procurement")

            .field("purchase_date", width=6)
            .field("received_date", width=6)

            .field("purchase_cost", width=6)
            .field("invoice_number", width=6)

            .section("Additional Information")

            .field("condition", width=6)
            .field("remarks", width=12)

            .submit(
                "Register Asset",
                icon="save",
            )

            .reverse(
                "assets:asset-list",
            )

            .build()
        )

        return PageDTO(
            title="Register Asset",
            subtitle="Register a new company asset",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Assets",
                    url=reverse(
                        "assets:asset-list",
                    ),
                ),
                BreadcrumbDTO(
                    label="Register",
                ),
            ],
            content=form_dto,
        )

    # =====================================================
    # Detail Page
    # =====================================================

    def detail_page(
        self,
        asset,
    ):

        form = AssetUpdateForm(
            instance=asset,
        )

        for field in form.fields.values():
            field.disabled = True

        form_dto = (
            FormBuilder(
                title="Asset Details",
                form=form,
            )

            .section("Asset Information")

            .field("company", width=6)
            .field("asset_model", width=6)

            .field("serial_number", width=6)

            .section("Procurement")

            .field("purchase_date", width=6)
            .field("received_date", width=6)

            .field("purchase_cost", width=6)
            .field("invoice_number", width=6)

            .section("Current Status")
            .field("condition", width=6)

            .section("Additional Information")

            .field("remarks", width=12)

            .section("System")

            .field("is_active", width=12)

            .reverse(
                "assets:asset-list",
            )

            .build()
        )

        return PageDTO(
            title="Asset Details",
            subtitle=asset.asset_tag,
            breadcrumb=[
                BreadcrumbDTO(
                    label="Assets",
                    url=reverse(
                        "assets:asset-list",
                    ),
                ),
                BreadcrumbDTO(
                    label=asset.asset_tag,
                ),
            ],
            toolbar=Toolbar(
                buttons=[
                    ToolbarButton(
                        label="Edit",
                        icon="bi-pencil",
                        url=reverse(
                            "assets:asset-update",
                            kwargs={
                                "pk": asset.pk,
                            },
                        ),
                        style="warning",
                    ),
                    ToolbarButton(
                        label="Back",
                        icon="bi-arrow-left",
                        url=reverse(
                            "assets:asset-list",
                        ),
                        style="secondary",
                    ),
                    ToolbarButton(
    label="Transfer",
    icon="bi-arrow-left-right",
    url=(
        reverse(
            "assets:asset-transfer-create",
        )
        + f"?asset={asset.pk}"
    ),
    style="warning",
),
ToolbarButton(
    label="History",
    icon="bi-clock-history",
    url=reverse(
        "assets:asset-history",
        kwargs={
            "pk": asset.pk,
        },
    ),
    style="secondary",
),
                ],
            ),
            
            content=form_dto,
        )

    # =====================================================
    # Update Page
    # =====================================================

    # =====================================================
# Update Page
# =====================================================

    def update_page(
        self,
        assignment,
        form=None,
    ):

        if form is None:
            form = AssetAssignmentUpdateForm(
                instance=assignment,
            )

        form_dto = (
            FormBuilder(
                title="Edit Assignment",
                form=form,
            )

            .section("Assignment Information")

            .field("employee", width=6)
            .field("site", width=6)

            .section("Assignment Dates")

            .field("assigned_date", width=6)
            .field("expected_return_date", width=6)

            .section("Remarks")

            .field("remarks", width=12)

            .section("System")

            .field("is_active", width=12)

            .submit(
                "Update Assignment",
                icon="save",
            )

            .reverse(
                "assets:asset-assignment-list",
            )

            .build()
        )

        assigned_to = (
            assignment.employee.full_name
            if assignment.employee
            else assignment.site.name
        )

        return PageDTO(
            title="Edit Assignment",

            subtitle=assignment.asset.asset_tag,

            description=[
                assignment.asset.asset_model.name,
                f"Assigned To: {assigned_to}",
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
                    label="Edit",
                ),
            ],

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