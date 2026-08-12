from core.dtos import (
    BreadcrumbDTO,
    PageDTO,
)

from core.ui.datagrid.builder import (
    DataGridBuilder,
)


class DataGridPageService:

    def build(self):

        grid = (

            DataGridBuilder("Demo Companies")

            .column(
                field="code",
                label="Code",
            )

            .column(
                field="name",
                label="Country",
            )

            .column(
                field="country",
                label="Country",
            )

            .column(
                field="status",
                label="Status",
            )

            .row(
                row_id=1,
                code="CMP001",
                name="Sun King Tanzania",
                country="Tanzania",
                status="Active",
            )

            .row(
                row_id=2,
                code="CMP002",
                name="Sun King Kenya",
                country="Kenya",
                status="Active",
            )

            .row(
                row_id=3,
                code="CMP003",
                name="Sun King Nigeria",
                country="Nigeria",
                status="Inactive",
            )

            .build()

        )

        return PageDTO(

            title="DataGrid",

            subtitle="Reusable enterprise data table component.",

            breadcrumb=[

                BreadcrumbDTO(
                    label="UI Library",
                    url="/ui/",
                ),

                BreadcrumbDTO(
                    label="DataGrid",
                ),

            ],

            content=grid,

        )