from core.dtos.modal import (
    ModalButtonDTO,
    ModalDTO,
)


class ModalBuilder:

    def __init__(
        self,
        modal_id: str,
        title: str,
    ):

        self.modal = ModalDTO(
            id=modal_id,
            title=title,
        )

    def body(
        self,
        body: str,
    ):

        self.modal.body = body

        return self

    def size(
        self,
        size: str,
    ):

        self.modal.size = size

        return self

    def scrollable(
        self,
        enabled=True,
    ):

        self.modal.scrollable = enabled

        return self

    def centered(
        self,
        enabled=True,
    ):

        self.modal.centered = enabled

        return self

    def static_backdrop(
        self,
        enabled=True,
    ):

        self.modal.static_backdrop = enabled

        return self

    def button(
        self,
        label,
        style="primary",
        type="button",
        url=None,
        icon=None,
        dismiss=False,
    ):

        self.modal.buttons.append(
            ModalButtonDTO(
                label=label,
                style=style,
                type=type,
                url=url,
                icon=icon,
                dismiss=dismiss,
            )
        )

        return self

    def build(self):

        return self.modal