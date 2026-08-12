from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from assets.models import Asset


class Command(BaseCommand):

    help = "Create Asset Management permission groups."

    def handle(self, *args, **options):

        content_type = ContentType.objects.get_for_model(
            Asset
        )

        permissions = {
            permission.codename: permission
            for permission in Permission.objects.filter(
                content_type=content_type,
            )
        }

        groups = {
            "Asset Administrator": [
                "view_asset",
                "add_asset",
                "change_asset",
                "delete_asset",
                "assign_asset",
                "transfer_asset",
                "export_asset",
            ],

            "Asset Manager": [
                "view_asset",
                "add_asset",
                "change_asset",
                "assign_asset",
                "transfer_asset",
                "export_asset",
            ],

            "Asset User": [
                "view_asset",
            ],
        }

        for group_name, permission_codes in groups.items():

            group, created = Group.objects.get_or_create(
                name=group_name,
            )

            group_permissions = []

            for codename in permission_codes:

                permission = permissions.get(codename)

                if permission is None:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Permission not found: {codename}"
                        )
                    )
                    continue

                group_permissions.append(permission)

            group.permissions.set(
                group_permissions
            )

            action = "Created" if created else "Updated"

            self.stdout.write(
                self.style.SUCCESS(
                    f"{action}: {group_name}"
                )
            )