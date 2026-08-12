from dataclasses import dataclass, field
from django.core.paginator import Page
from typing import Any


@dataclass(slots=True, frozen=True)
class GridColumn:

    field: str
    label: str
    sortable: bool = True
    width: str | None = None
    align: str = "start"
    component: str = "text"


@dataclass(slots=True, frozen=True)
class GridAction:

    title: str
    icon: str
    url_name: str
    css_class: str = "btn btn-sm btn-outline-secondary"
    method: str = "GET"
    confirm_message: str | None = None
    permission: str | None = None


@dataclass(slots=True, frozen=True)
class GridCell:
    value: Any
    display: str
    renderer: str = "text"
    css_class: str | None = None
    url: str | None = None


@dataclass(slots=True, frozen=True)
class GridRow:

    id: Any
    cells: dict[str, GridCell]


@dataclass(slots=True)
class DataGrid:

    title: str

    template: str = "components/datagrid.html"

    columns: list[GridColumn] = field(default_factory=list)

    rows: list[GridRow] = field(default_factory=list)

    actions: list[GridAction] = field(default_factory=list)

    page: Any = None

    selectable: bool = True

    searchable: bool = True

    sortable: bool = True

    search_placeholder: str = "Search..."

    search_query: str = ""

    search_url: str | None = None
    def filter_permissions(self, user):

        from core.ui.actions.permissions import (
            ActionPermissionService,
        )

        if user.is_superuser:
            return self

        self.actions = ActionPermissionService.filter(
            self.actions,
            user,
        )

        return self
