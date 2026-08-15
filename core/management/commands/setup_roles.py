from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

from accounts.models import User
from accounts.models.choices import UserType
from core.permissions.role_permissions import ROLE_PERMISSIONS


class Command(BaseCommand):
    help = "Configure V2 role groups and synchronize users."

    ROLE_GROUPS = {
        UserType.SUPER_ADMIN: "SUPER_ADMIN",
        UserType.ADMIN: "ADMIN",
        UserType.COUNTRY_ADMIN: "COUNTRY_ADMIN",
        UserType.USER: "USER",
    }

    LEGACY_GROUPS = {
        "Asset Administrator",
        "Asset Manager",
        "Asset User",
    }

    def handle(self, *args, **options):

        self.stdout.write(
            self.style.NOTICE(
                "Configuring V2 role permissions..."
            )
        )

        # -------------------------------------------------
        # Create / update role groups
        # -------------------------------------------------

        groups = {}

        for user_type, group_name in self.ROLE_GROUPS.items():

            group, created = Group.objects.get_or_create(
                name=group_name,
            )

            groups[user_type] = group

            permissions = ROLE_PERMISSIONS.get(
                user_type,
                [],
            )

            if permissions == "__ALL__":

                group.permissions.set(
                    Permission.objects.all()
                )

            else:

                permission_objects = []

                for permission_name in permissions:

                    try:
                        app_label, codename = (
                            permission_name.split(".", 1)
                        )
                    except ValueError:

                        self.stdout.write(
                            self.style.WARNING(
                                f"Invalid permission: "
                                f"{permission_name}"
                            )
                        )

                        continue

                    permission = (
                        Permission.objects
                        .filter(
                            content_type__app_label=app_label,
                            codename=codename,
                        )
                        .first()
                    )

                    if permission is None:

                        self.stdout.write(
                            self.style.WARNING(
                                f"Permission not found: "
                                f"{permission_name}"
                            )
                        )

                        continue

                    permission_objects.append(
                        permission
                    )

                group.permissions.set(
                    permission_objects
                )

            action = "Created" if created else "Updated"

            self.stdout.write(
                self.style.SUCCESS(
                    f"{action} role: {group_name}"
                )
            )

        # -------------------------------------------------
        # Synchronize users
        # -------------------------------------------------

        synchronized = 0

        for user in User.objects.all():

            group = groups.get(
                user.user_type
            )

            if group is None:

                self.stdout.write(
                    self.style.WARNING(
                        f"Unknown user role for "
                        f"{user.username}: "
                        f"{user.user_type}"
                    )
                )

                continue

            # Remove legacy V1 groups.
            user.groups.remove(
                *Group.objects.filter(
                    name__in=self.LEGACY_GROUPS
                )
            )

            # Remove V2 role groups so the user's role
            # always maps cleanly to exactly one role.
            user.groups.remove(
                *groups.values()
            )

            # Add current role group.
            user.groups.add(group)

            synchronized += 1

            self.stdout.write(
                f"  {user.username}: "
                f"{user.user_type} → {group.name}"
            )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Role setup complete. "
                f"Synchronized {synchronized} user(s)."
            )
        )