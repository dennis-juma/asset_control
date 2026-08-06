from core.permissions.providers.django_provider import (
    DjangoPermissionProvider,
)


class PermissionService:

    provider = DjangoPermissionProvider()

    @classmethod
    def can(
        cls,
        user,
        permission,
    ):

        return cls.provider.has_permission(
            user,
            permission,
        )

    @classmethod
    def require(
        cls,
        user,
        permission,
    ):

        if not cls.can(user, permission):

            raise PermissionDenied()