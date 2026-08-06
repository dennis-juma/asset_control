from core.docs.dtos import (
    DocumentationDTO,
    DocumentationSectionDTO,
)


class DocumentationBuilder:

    def __init__(
        self,
        title: str,
        slug: str,
        description: str,
    ):

        self.document = DocumentationDTO(
            title=title,
            slug=slug,
            description=description,
        )

    def category(
    self,
    category: str,
):

        self.document.category = category

        return self

    def version(
        self,
        version: str,
    ):

        self.document.version = version

        return self

    def icon(
        self,
        icon: str,
    ):

        self.document.icon = icon

        return self

    def section(

        self,

        title,

        component,

        content=None,

        description=None,

    ):

        self.document.sections.append(

            DocumentationSectionDTO(

                title=title,

                component=component,

                content=content,

                description=description,

                order=len(self.document.sections) + 1,

            )

        )

        return self

    def related(
        self,
        *items,
    ):

        self.document.related.extend(items)

        return self


    def navigation(
        self,
        *items,
    ):

        self.document.navigation.extend(items)

        return self

    def build(self):

        return self.document