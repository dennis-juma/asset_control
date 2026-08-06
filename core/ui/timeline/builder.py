from collections import defaultdict

from core.dtos.timeline import (
    TimelineDTO,
    TimelineGroupDTO,
    TimelineItemDTO,
)


class TimelineBuilder:

    def __init__(self):

        self._items = []

    def add(self, item: TimelineItemDTO):

        self._items.append(item)

        return self

    def build(self):

        groups = defaultdict(list)

        for item in sorted(
            self._items,
            key=lambda x: x.occurred_at,
            reverse=True,
        ):

            key = item.occurred_at.strftime("%d %B %Y")

            groups[key].append(item)

        return TimelineDTO(
            groups=[
                TimelineGroupDTO(
                    date=date,
                    items=items,
                )
                for date, items in groups.items()
            ]
        )