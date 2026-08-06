from django.urls import reverse

from dashboard.dto.quick_action import QuickActionDTO


class QuickActionService:
    """
    Provides quick dashboard actions.
    """

    def get_actions(self) -> list[QuickActionDTO]:
        return [
            QuickActionDTO(
                title="Register Asset",
                icon="bi bi-laptop",
                url="#",
                color="primary",
            ),
            QuickActionDTO(
                title="Assign Asset",
                icon="bi bi-person-check",
               url="#",
                color="success",
            ),
            QuickActionDTO(
                title="Return Asset",
                icon="bi bi-arrow-return-left",
                url="#",
                color="warning",
            ),
            QuickActionDTO(
                title="Schedule Maintenance",
                icon="bi bi-tools",
                url="#",
                color="info",
            ),
            QuickActionDTO(
                title="Employees",
                icon="bi bi-people",
                url="#",
                color="secondary",
            ),
        ]