from core.docs.registry import (
    registry,
    DocumentMetadata,
)
from core.docs.builders import DocumentationBuilder

registry.register(

    DocumentMetadata(

        slug="datagrid",

        title="DataGrid",

        category="UI Components",

        icon="table",

        module="core.docs.documents.datagrid",

    )

)

from core.docs.builders import DocumentationBuilder


def build():

    return (

        DocumentationBuilder(

            title="DataGrid",

            slug="datagrid",

            description="Reusable enterprise data table component.",

        )

        .category("UI Components")

        .icon("table")

        .version("1.0")

        .section(

            title="Overview",

            component="markdown",

            content="""
DataGrid is a reusable table component used
throughout the Asset Management System.

It supports:

• Search

• Pagination

• Sorting

• Actions

• Responsive layouts

""",

        )

        .section(

            title="Features",

            component="checklist",

            content=[

                "Search",

                "Pagination",

                "Sorting",

                "Actions",

                "Responsive",

            ],

        )

        .section(

            title="Builder Example",

            component="code",

            content="""
grid = (
    DataGridBuilder("Companies")
        .column(field="code", label="Code")
        .column(field="name", label="Company")
        .row(
            row_id=1,
            code="CMP001",
            name="Sun King",
        )
        .build()
)
""",

        )

        .section(

            title="Properties",

            component="table",

            content=[

                ("title", "Grid title"),

                ("columns", "Grid columns"),

                ("rows", "Grid rows"),

                ("actions", "Action buttons"),

                ("page", "Pagination object"),

                ("searchable", "Enable search"),

                ("sortable", "Enable sorting"),

            ],

        )

        .section(

            title="Methods",

            component="table",

            content=[

                ("column()", "Add column"),

                ("row()", "Add row"),

                ("action()", "Add action"),

                ("search()", "Enable search"),

                ("paginate()", "Attach paginator"),

                ("build()", "Return DataGrid"),

            ],

        )

        .section(

            title="Roadmap",

            component="checklist",

            content=[

                "✓ Search",

                "✓ Pagination",

                "✓ CRUD Actions",

                "🚧 Sorting",

                "🚧 Export",

                "🚧 Bulk Actions",

            ],

        )

        .build()

    )