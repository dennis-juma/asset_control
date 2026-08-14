from django.urls import reverse

from core.permissions.constants import Permissions
from core.dtos.asset_attachments import (
    AssetAttachmentsContentDTO,
)
from assets.forms import (
    AssetCreateForm,
    AssetUpdateForm,
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
        country_context=None,
    ):

        assets = self.repository.list(
            query=query,
            page=page,
            country_context=country_context,
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
            field="country",
            label="Country",
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
                country=asset.country.name,
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
            subtitle="Manage Country Assets",
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
                        permission=Permissions.ASSET_CREATE,
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

            .field("country", width=6)
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
            subtitle="Register a new country asset",
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

            .field("country", width=6)
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
                         permission=Permissions.ASSET_UPDATE,
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
     permission=Permissions.ASSET_TRANSFER,
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
     permission=Permissions.ASSET_VIEW,
),
                ],
            ),
            
            content=form_dto,
            extra_content=AssetAttachmentsContentDTO(
        asset=asset,
        attachments=asset.attachments.all(),
    )
        )

    # =====================================================
    # Update Page
    # =====================================================

    # =====================================================
# Update Page
# =====================================================

    def update_page(self, asset, form=None):
        if form is None:
            form = AssetUpdateForm(instance=asset)

        form_dto = (
            FormBuilder(title="Edit Asset", form=form)
            .section("Asset Information")
            .field("country", width=6)
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
            .section("System")
            .field("is_active", width=12)
            .submit("Update Asset", icon="save")
            .reverse("assets:asset-detail", kwargs={"pk": asset.pk})
            .build()
        )

        return PageDTO(
            title="Edit Asset",
            subtitle=asset.asset_tag,
            breadcrumb=[
                BreadcrumbDTO(
                    label="Assets",
                    url=reverse("assets:asset-list"),
                ),
                BreadcrumbDTO(
                    label=asset.asset_tag,
                    url=reverse(
                        "assets:asset-detail",
                        kwargs={"pk": asset.pk},
                    ),
                ),
                BreadcrumbDTO(label="Edit"),
            ],
            content=form_dto,
        )
