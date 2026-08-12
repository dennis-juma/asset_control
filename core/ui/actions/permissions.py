from core.permissions.service import PermissionService


class ActionPermissionService:

    @staticmethod
    def filter(actions, user):

        if user.is_superuser:
            return actions

        visible = []

        for action in actions:

            permission = getattr(
                action,
                "permission",
                None,
            )

            if not permission:
                visible.append(action)
                continue

            if PermissionService.can(
                user,
                permission,
            ):
                visible.append(action)

        return visible