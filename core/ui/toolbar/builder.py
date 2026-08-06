from core.dtos.toolbar import (
    BulkAction,
    Toolbar,
    ToolbarButton,
)
from core.exports.enums import ExportType


class ToolbarBuilder:

    def __init__(self, title=""):

        self.toolbar = Toolbar(title=title)

    def button(
        self,
        label,
        icon,
        url="#",
        style="primary",
        permission=None,
        method="GET",
    ):

        self.toolbar.buttons.append(
            ToolbarButton(
                label=label,
                icon=icon,
                url=url,
                style=style,
                permission=permission,
                method=method,
            )
        )

        return self

    def bulk_action(
        self,
        value,
        label,
    ):

        self.toolbar.bulk_actions.append(
            BulkAction(
                value=value,
                label=label,
            )
        )

        return self

    def enable_export(formats=[
        ExportType.EXCEL,
        ExportType.CSV,
        ExportType.PDF,
        
    ]):

        self.toolbar.show_export = True
        self.toolbar.export_formats = formats

        return self

    def enable_import(self):

        self.toolbar.show_import = True

        return self

    def disable_refresh(self):

        self.toolbar.show_refresh = False

        return self

    def build(self):

        return self.toolbar