from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class ToolbarButton:

    label: str

    icon: str

    url: str = "#"

    style: str = "primary"

    permission: str | None = None

    method: str = "GET"


@dataclass(slots=True, frozen=True)
class BulkAction:

    value: str

    label: str


@dataclass(slots=True, frozen=True)
class Toolbar:

    title: str = ""

    buttons: list[ToolbarButton] = field(default_factory=list)

    bulk_actions: list[BulkAction] = field(default_factory=list)

    show_refresh: bool = True

    show_export: bool = False

    show_import: bool = False

    def filter_permissions(self, user):

        from core.ui.actions.permissions import (
            ActionPermissionService,
        )

        return Toolbar(
            title=self.title,
            buttons=ActionPermissionService.filter(
                self.buttons,
                user,
            ),
            bulk_actions=self.bulk_actions,
            show_refresh=self.show_refresh,
            show_export=self.show_export,
            show_import=self.show_import,
        )