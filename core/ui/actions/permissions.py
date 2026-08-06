class ActionPermissionService:

    @staticmethod
    def filter(actions, user):

        if user.is_superuser:
            return actions

        visible = []

        for action in actions:

            if not action.permission:
                visible.append(action)
                continue

            if user.has_perm(action.permission):
                visible.append(action)

        return visible