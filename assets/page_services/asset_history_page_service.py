from django.urls import reverse

from assets.repositories import AssetHistoryRepository

from core.dtos.page import (
    PageDTO,
    BreadcrumbDTO,
)

from core.ui.datagrid.builder import DataGridBuilder


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

        for event in history:

            status = ""

            if (
                event.old_status
                or event.new_status
            ):
                status = (
                    f"{event.get_old_status_display()}"
                    f" → "
                    f"{event.get_new_status_display()}"
                )

            employee = (
                str(event.employee)
                if event.employee
                else "—"
            )

            site = (
                str(event.site)
                if event.site
                else "—"
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