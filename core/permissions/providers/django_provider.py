class DjangoPermissionProvider:

    @staticmethod
    def has_permission(
        user,
        permission,
    ):

        return user.has_perm(permission)