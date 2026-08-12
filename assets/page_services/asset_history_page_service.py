from django.urls import reverse

from assets.forms import AssetHistoryDetailForm
from assets.repositories import AssetHistoryRepository

from core.dtos.page import (
    PageDTO,
    BreadcrumbDTO,
)

from core.ui.datagrid.builder import DataGridBuilder
from core.ui.forms.builder import FormBuilder   


class AssetHistoryPageService:

    def __init__(self):
        self.repository = AssetHistoryRepository()

    def list_page(
        self,
        asset,
        query="",
        page=1,
    ):

        history = self.repository.list(
            asset=asset,
            query=query,
            page=page,
        )

        grid = DataGridBuilder(
            "Asset History"
        )

        grid.column(
            field="event_date",
            label="Date",
        )

        grid.column(
            field="event_type",
            label="Event",
        )

        grid.column(
            field="employee",
            label="Employee",
        )

        grid.column(
            field="site",
            label="Site",
        )

        grid.column(
            field="status",
            label="Status",
        )

        grid.column(
            field="performed_by",
            label="Performed By",
        )

        grid.action(
    title="View",
    icon="bi-eye",
    url_name="assets:asset-history-detail",
)

        for event in history:

            status = ""

            if (
                event.old_status
                or event.new_status
            ):
                status = (
                    f"{event.get_old_status_display()}"
                    f" â†’ "
                    f"{event.get_new_status_display()}"
                )

            employee = (
                str(event.employee)
                if event.employee
                else "â€”"
            )

            site = (
                str(event.site)
                if event.site
                else "â€”"
            )

            performed_by = (
                str(event.performed_by)
                if event.performed_by
                else "System"
            )

            grid.row(
                row_id=event.pk,

                event_date=event.event_date.strftime(
                    "%d %b %Y %H:%M"
                ),

                event_type=event.get_event_type_display(),

                employee=employee,

                site=site,

                status=status,

                performed_by=performed_by,
            )

        grid.paginate(history)

        return PageDTO(
            title="Asset History",

            subtitle=(
                f"Lifecycle history for "
                f"{asset.asset_tag}"
            ),

            breadcrumb=[
                BreadcrumbDTO(
                    label="Assets",
                ),

                BreadcrumbDTO(
                    label=asset.asset_tag,
                    url=reverse(
                        "assets:asset-detail",
                        kwargs={
                            "pk": asset.pk,
                        },
                    ),
                ),

                BreadcrumbDTO(
                    label="History",
                ),
            ],

            content=grid.build(),
        )


    def detail_page(
    self,
    history,
):

        form = AssetHistoryDetailForm(
            instance=history,
        )

        # History records are read-only
        for field in form.fields.values():
            field.disabled = True

        
        form_dto = (
            FormBuilder(
                title="History Event",
                form=form,
            )

            .section(
                "Event Information",
                description="Details of the asset lifecycle event.",
            )

            .field(
                "event_type",
                width=6,
            )

            .field(
                "event_date",
                width=6,
            )

            .section(
                "Asset Context",
            )

            .field(
                "asset",
                width=6,
            )

            .field(
                "country",
                width=6,
            )

            .section(
                "Assignment / Location",
            )

            .field(
                "employee",
                width=6,
            )

            .field(
                "site",
                width=6,
            )

            .field(
                "performed_by",
                width=6,
            )

            .section(
                "Status Change",
            )

            .field(
                "old_status",
                width=6,
            )

            .field(
                "new_status",
                width=6,
            )

            .section(
                "Audit Information",
            )

            .field(
                "reference",
                width=6,
            )

            .field(
                "notes",
                width=12,
            )

            .field(
                "metadata",
                width=12,
            )

            .reverse(
                "assets:asset-history",
                kwargs={
                    "pk": history.asset.pk,
                },
                label="Back to History",
            )

            .build()
        )

        return PageDTO(
            title="History Event",

            subtitle=(
                f"{history.asset.asset_tag} - "
                f"{history.get_event_type_display()}"
            ),

            breadcrumb=[
                BreadcrumbDTO(
                    label="Assets",
                    url=reverse(
                        "assets:asset-list",
                    ),
                ),

                BreadcrumbDTO(
                    label=history.asset.asset_tag,
                    url=reverse(
                        "assets:asset-detail",
                        kwargs={
                            "pk": history.asset.pk,
                        },
                    ),
                ),

                BreadcrumbDTO(
                    label="History",
                    url=reverse(
                        "assets:asset-history",
                        kwargs={
                            "pk": history.asset.pk,
                        },
                    ),
                ),

                BreadcrumbDTO(
                    label="Event",
                ),
            ],

            content=form_dto,
        )