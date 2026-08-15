

from .dtos import (
    DataGrid,
    GridAction,
    GridCell,
    GridColumn,
    GridRow,
)
class DataGridBuilder:

    def __init__(self, title: str):

        self.grid = DataGrid(title=title)

    def column(self, **kwargs):

        self.grid.columns.append(GridColumn(**kwargs))

        return self

    def row(self, row_id, **cells):

        values = {}

        for key, value in cells.items():

            if isinstance(value, GridCell):

                values[key] = value

            elif isinstance(value, tuple):

                cell_value, renderer = value

                values[key] = renderer.render(cell_value)

            else:

                values[key] = GridCell(
                    value=value,
                    display="" if value is None else str(value),
                )

        self.grid.rows.append(
            GridRow(
                id=row_id,
                cells=values,
            )
        )

        return self

    def action(self, **kwargs):

        self.grid.actions.append(
            GridAction(**kwargs)
        )

        return self

    def selectable(self, enabled=True):

        self.grid.selectable = enabled

        return self

    def paginate(self, page):

        self.grid.page = page

        return self

    def bulk_update(self, url_name, selection_label="records"):

        self.grid.bulk_update_url = url_name
        self.grid.selection_label = selection_label

        return self

    def build(self):

        return self.grid


    def search(
    self,
    url,
    query="",
    placeholder="Search...",
):

        self.grid.search_url = url
        self.grid.search_query = query
        self.grid.search_placeholder = placeholder

        return self
