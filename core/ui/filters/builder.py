from core.dtos.filters import (
    FilterBar,
    FilterField,
    FilterOption,
)


class FilterBuilder:

    def __init__(self):

        self.fields = []

    def search(
        self,
        name="search",
        label="Search",
        placeholder="Search...",
        value="",
    ):

        self.fields.append(
            FilterField(
                name=name,
                label=label,
                type="search",
                value=value,
                placeholder=placeholder,
            )
        )

        return self

    def select(
        self,
        name,
        label,
        options,
        value=None,
    ):

        opts = [
            FilterOption(
                value=str(v),
                label=l,
            )
            for v, l in options
        ]

        self.fields.append(
            FilterField(
                name=name,
                label=label,
                type="select",
                value=value,
                options=opts,
            )
        )

        return self

    def date(
        self,
        name,
        label,
        value=None,
    ):

        self.fields.append(
            FilterField(
                name=name,
                label=label,
                type="date",
                value=value,
            )
        )

        return self

    def build(self):

        return FilterBar(
            fields=self.fields,
        )