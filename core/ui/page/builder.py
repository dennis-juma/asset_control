from core.dtos.page import (
    BreadcrumbDTO,
    PageDTO,
)


class PageBuilder:

    def __init__(
        self,
        title,
        subtitle=None,
    ):

        self.page = PageDTO(
            title=title,
            subtitle=subtitle,
        )

    def breadcrumb(
        self,
        label,
        url=None,
    ):

        self.page.breadcrumb.append(
            BreadcrumbDTO(
                label=label,
                url=url,
            )
        )

        return self

    def toolbar(
        self,
        toolbar,
    ):

        self.page.toolbar = toolbar

        return self

    def statistics(
        self,
        cards,
    ):

        self.page.statistics = cards

        return self

    def filters(
        self,
        filters,
    ):

        self.page.filters = filters

        return self

    def content(
        self,
        content,
    ):

        self.page.content = content

        return self

    def sidebar(
        self,
        sidebar,
    ):

        self.page.sidebar = sidebar

        return self

    def build(self):

        return self.page