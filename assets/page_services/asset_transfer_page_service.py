from django.urls import reverse

from assets.forms.transfer import (
    AssetTransferCreateForm,
    AssetTransferUpdateForm,
)
from assets.repositories import AssetTransferRepository

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


class AssetTransferPageService:

    def __init__(self):
        self.repository = AssetTransferRepository()

    # =====================================================
    # Helpers
    # =====================================================

    @staticmethod
    def _get_source_name(transfer):

        if transfer.from_employee:
            return transfer.from_employee.full_name

        if transfer.from_site:
            return transfer.from_site.name

        return "Unknown"

    @staticmethod
    def _get_target_name(transfer):

        if transfer.to_employee:
            return transfer.to_employee.full_name

        if transfer.to_site:
            return transfer.to_site.name

        return "Unknown"

    # =====================================================
    # List Page
    # =====================================================

    def list_page(
    self,
    query="",
    page=1,
):

        transfers = self.repository.list(
            query=query,
            page=page,
        )

        grid = DataGridBuilder(
            "Asset Transfers"
        )

        grid.column(
            field="asset_tag",
            label="Asset Tag",
        )

        grid.column(
            field="from_name",
            label="From",
        )

        grid.column(
            field="to_name",
            label="To",
        )

        grid.column(
            field="transfer_date",
            label="Transfer Date",
        )

        grid.column(
            field="reason",
            label="Reason",
        )

        for transfer in transfers:

            grid.row(
                row_id=transfer.pk,
                asset_tag=transfer.asset.asset_tag,
                from_name=self._get_source_name(
                    transfer,
                ),
                to_name=self._get_target_name(
                    transfer,
                ),
                transfer_date=transfer.transfer_date,
                reason=transfer.reason,
            )

        grid.action(
            title="View",
            icon="bi-eye",
            url_name="assets:asset-transfer-detail",
        )

        grid.action(
            title="Edit",
            icon="bi-pencil",
            url_name="assets:asset-transfer-update",
        )

        grid.paginate(
            transfers,
        )

        return PageDTO(
            title="Asset Transfers",
            subtitle="View asset transfer history",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Assets",
                    url=reverse(
                        "assets:asset-list",
                    ),
                ),
                BreadcrumbDTO(
                    label="Transfers",
                ),
            ],
            toolbar=Toolbar(
                buttons=[
                    ToolbarButton(
                        label="Transfer Asset",
                        icon="bi-arrow-left-right",
                        url=reverse(
                            "assets:asset-transfer-create",
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
    asset=None,
    previous_assignment=None,
):

        if form is None:

            form = AssetTransferCreateForm(
                asset=asset,
                previous_assignment=previous_assignment,
            )

        form_action = ""

        if asset is not None:
            form_action = (
                reverse(
                    "assets:asset-transfer-create",
                )
                + f"?asset={asset.pk}"
            )

        form_dto = (
            FormBuilder(
                title="Transfer Asset",
                form=form,
                action=form_action,
            )

            .section(
                "Transfer To",
                description="Select the new employee or site.",
            )

            .field(
                "assignment_type",
                width=12,
            )

            .field(
                "employee",
                width=6,
            )

            .field(
                "site",
                width=6,
            )

            .section(
                "Transfer Information",
            )

            .field(
                "transfer_date",
                width=6,
            )

            .field(
                "reason",
                width=6,
            )

            .field(
                "remarks",
                width=12,
            )

            .submit(
                "Transfer Asset",
                icon="bi-arrow-left-right",
            )

            .reverse(
                "assets:asset-transfer-list",
            )

            .build()
        )

        return PageDTO(
            title="Transfer Asset",
            subtitle="Transfer an assigned asset to another employee or site.",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Assets",
                    url=reverse(
                        "assets:asset-list",
                    ),
                ),
                BreadcrumbDTO(
                    label="Transfers",
                    url=reverse(
                        "assets:asset-transfer-list",
                    ),
                ),
                BreadcrumbDTO(
                    label="Transfer Asset",
                ),
            ],
            content=form_dto,
        )



   # =====================================================
    # Detail Page
    # =====================================================

    def detail_page(
        self,
        transfer,
    ):

        form = AssetTransferUpdateForm(
            instance=transfer,
        )

        # Detail page is read-only
        for field in form.fields.values():
            field.disabled = True

        form_dto = (
            FormBuilder(
                title="Transfer Details",
                form=form,
            )

            .section(
                "Transfer Information",
            )

            .field(
                "transfer_date",
                width=6,
            )

            .field(
                "reason",
                width=6,
            )

            .field(
                "remarks",
                width=12,
            )

            .field(
                "is_active",
                width=12,
            )

            .reverse(
                "assets:asset-transfer-list",
            )

            .build()
        )

        return PageDTO(
            title="Asset Transfer",
            subtitle=transfer.asset.asset_tag,

            breadcrumb=[
                BreadcrumbDTO(
                    label="Assets",
                    url=reverse(
                        "assets:asset-list",
                    ),
                ),

                BreadcrumbDTO(
                    label="Transfers",
                    url=reverse(
                        "assets:asset-transfer-list",
                    ),
                ),

                BreadcrumbDTO(
                    label=transfer.asset.asset_tag,
                ),
            ],

            toolbar=Toolbar(
                buttons=[
                    ToolbarButton(
                        label="Edit",
                        icon="bi-pencil",
                        url=reverse(
                            "assets:asset-transfer-update",
                            kwargs={
                                "pk": transfer.pk,
                            },
                        ),
                        style="warning",
                    ),

                    ToolbarButton(
                        label="Back",
                        icon="bi-arrow-left",
                        url=reverse(
                            "assets:asset-transfer-list",
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

    def update_page(
        self,
        transfer,
        form=None,
    ):

        if form is None:

            form = AssetTransferUpdateForm(
                instance=transfer,
            )

        form_dto = (
            FormBuilder(
                title="Edit Transfer",
                form=form,
            )

            .section("Transfer Information")

            .field(
                "transfer_date",
                width=6,
            )

            .field(
                "reason",
                width=6,
            )

            .field(
                "remarks",
                width=12,
            )

            .field(
                "is_active",
                width=12,
            )

            .submit(
                "Update",
                icon="bi-save",
            )

            .reverse(
                "assets:asset-transfer-detail",
                kwargs={
                    "pk": transfer.pk,
                },
            )

            .build()
        )

        return PageDTO(
            title="Edit Transfer",
            subtitle=transfer.asset.asset_tag,

            breadcrumb=[
                BreadcrumbDTO(
                    label="Assets",
                    url=reverse(
                        "assets:asset-list",
                    ),
                ),
                BreadcrumbDTO(
                    label="Transfers",
                    url=reverse(
                        "assets:asset-transfer-list",
                    ),
                ),
                BreadcrumbDTO(
                    label=transfer.asset.asset_tag,
                    url=reverse(
                        "assets:asset-transfer-detail",
                        kwargs={
                            "pk": transfer.pk,
                        },
                    ),
                ),
                BreadcrumbDTO(
                    label="Edit",
                ),
            ],

            content=form_dto,
        )