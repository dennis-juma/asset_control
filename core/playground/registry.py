from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class UIComponent:

    name: str

    description: str

    icon: str

    url: str

    category: str


UI_COMPONENTS = [

    UIComponent(
        name="DataGrid",
        description="Enterprise data tables.",
        icon="table",
        url="ui:datagrid",
        category="Data Display",
    ),

    UIComponent(
        name="Forms",
        description="Reusable form builder.",
        icon="file-earmark-text",
        url="ui:forms",
        category="Forms",
    ),

    UIComponent(
        name="Buttons",
        description="Button styles.",
        icon="hand-index-thumb",
        url="ui:buttons",
        category="Controls",
    ),

    UIComponent(
        name="Cards",
        description="Dashboard cards.",
        icon="grid",
        url="ui:cards",
        category="Data Display",
    ),
]