from django.db import migrations


def migrate_user_roles_and_country_access(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    UserCountryAccess = apps.get_model(
        "accounts",
        "UserCountryAccess",
    )

    role_mapping = {
        "SUPER_ADMIN": "SUPER_ADMIN",
        "ADMIN": "ADMIN",
        "IT_MANAGER": "COUNTRY_ADMIN",
        "STORE_MANAGER": "USER",
        "AUDITOR": "USER",
        "EMPLOYEE": "USER",
    }

    for user in User.objects.all():

        old_role = user.user_type

        new_role = role_mapping.get(
            old_role,
            "USER",
        )

        user.user_type = new_role
        user.save(
            update_fields=["user_type"],
        )

        # SUPER_ADMIN has global access and does not
        # require country-access records.
        if new_role == "SUPER_ADMIN":
            continue

        try:
            employee = user.employee
        except User.employee.RelatedObjectDoesNotExist:
            employee = None

        if employee and employee.country_id:
            UserCountryAccess.objects.get_or_create(
                user_id=user.pk,
                country_id=employee.country_id,
            )


def reverse_user_roles_and_country_access(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    UserCountryAccess = apps.get_model(
        "accounts",
        "UserCountryAccess",
    )

    # Remove generated country access records.
    UserCountryAccess.objects.all().delete()

    # Reverse only the role mappings that are unambiguous.
    reverse_mapping = {
        "SUPER_ADMIN": "SUPER_ADMIN",
        "ADMIN": "ADMIN",
        "COUNTRY_ADMIN": "IT_MANAGER",
        "USER": "EMPLOYEE",
    }

    for user in User.objects.all():
        user.user_type = reverse_mapping.get(
            user.user_type,
            "EMPLOYEE",
        )
        user.save(
            update_fields=["user_type"],
        )


class Migration(migrations.Migration):

    dependencies = [
        (
            "accounts",
            "0002_alter_user_user_type_usercountryaccess",
        ),
    ]

    operations = [
        migrations.RunPython(
            migrate_user_roles_and_country_access,
            reverse_user_roles_and_country_access,
        ),
    ]