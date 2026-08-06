from core.docs.builders import DocumentationBuilder
from core.docs.registry import DocumentMetadata, registry


registry.register(
    DocumentMetadata(
        slug="form-builder",
        title="Form Builder",
        category="UI Components",
        icon="file-earmark-text",
        module="core.docs.documents.form_builder",
    )
)


def build():

    return (

        DocumentationBuilder(

            title="Form Builder",

            slug="form-builder",

            description="Reusable builder for Django forms.",

        )

        .category("UI Components")

        .icon("file-earmark-text")

        .version("1.0")

        .section(

            title="Overview",

            component="markdown",

            content="""
FormBuilder provides a consistent way of creating
forms across the application.

It supports sections, actions and responsive layouts.
""",

        )

        .section(

            title="Features",

            component="checklist",

            content=[

                "Responsive Layout",

                "Sections",

                "Validation",

                "File Upload",

                "Custom Buttons",

            ],

        )

        .section(

            title="Builder Example",

            component="code",

            content="""
form = (
    FormBuilder(
        title="Create Company",
        form=form,
    )
    .section("General")
        .field("name")
        .field("email")
    .submit("Save")
    .build()
)
""",

        )

        .section(

            title="Methods",

            component="table",

            content=[

                ("section()", "Create section"),

                ("field()", "Add field"),

                ("submit()", "Submit button"),

                ("cancel()", "Cancel button"),

                ("build()", "Return FormDTO"),

            ],

        )

        .section(

            title="Roadmap",

            component="checklist",

            content=[

                "✓ Sections",

                "✓ Validation",

                "✓ Responsive",

                "🚧 Tabs",

                "🚧 Wizard",

            ],

        )

        .build()

    )
