from core.dtos.actions import (
    ActionDTO,
    ActionMethod,
    ActionTarget,
)


class ActionBuilder:

    def __init__(self):

        self.actions = []

    def add(
        self,
        label,
        icon,
        url,
        method=ActionMethod.GET,
        permission=None,
        target=ActionTarget.SELF,
        confirmation=None,
        danger=False,
        visible=True,
    ):

        self.actions.append(
            ActionDTO(
                label=label,
                icon=icon,
                url=url,
                method=method,
                permission=permission,
                target=target,
                confirmation=confirmation,
                danger=danger,
                visible=visible,
            )
        )

        return self

    def build(self):

        return self.actions