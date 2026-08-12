from django.db import migrations, models


def migrate_in_stock_to_available(apps, schema_editor):
    Asset = apps.get_model("assets", "Asset")
    AssetHistory = apps.get_model("assets", "AssetHistory")

    Asset.objects.filter(status="IN_STOCK").update(status="AVAILABLE")
    AssetHistory.objects.filter(old_status="IN_STOCK").update(
        old_status="AVAILABLE"
    )
    AssetHistory.objects.filter(new_status="IN_STOCK").update(
        new_status="AVAILABLE"
    )


def migrate_available_to_in_stock(apps, schema_editor):
    Asset = apps.get_model("assets", "Asset")
    AssetHistory = apps.get_model("assets", "AssetHistory")

    Asset.objects.filter(status="AVAILABLE").update(status="IN_STOCK")
    AssetHistory.objects.filter(old_status="AVAILABLE").update(
        old_status="IN_STOCK"
    )
    AssetHistory.objects.filter(new_status="AVAILABLE").update(
        new_status="IN_STOCK"
    )


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0014_alter_asset_options"),
    ]

    operations = [
        migrations.RunPython(
            migrate_in_stock_to_available,
            migrate_available_to_in_stock,
        ),
        migrations.AlterField(
            model_name="asset",
            name="status",
            field=models.CharField(
                choices=[
                    ("AVAILABLE", "Available"),
                    ("ASSIGNED", "Assigned"),
                    ("RESERVED", "Reserved"),
                    ("IN_TRANSIT", "In Transit"),
                    ("MAINTENANCE", "Under Preventive Maintenance"),
                    ("UNDER_REPAIR", "Under Repair"),
                    ("STOLEN", "Stolen"),
                    ("LOST", "Lost"),
                    ("RETIRED", "Retired"),
                    ("DISPOSED", "Disposed"),
                ],
                default="AVAILABLE",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="assethistory",
            name="old_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("AVAILABLE", "Available"),
                    ("ASSIGNED", "Assigned"),
                    ("RESERVED", "Reserved"),
                    ("IN_TRANSIT", "In Transit"),
                    ("MAINTENANCE", "Under Preventive Maintenance"),
                    ("UNDER_REPAIR", "Under Repair"),
                    ("STOLEN", "Stolen"),
                    ("LOST", "Lost"),
                    ("RETIRED", "Retired"),
                    ("DISPOSED", "Disposed"),
                ],
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="assethistory",
            name="new_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("AVAILABLE", "Available"),
                    ("ASSIGNED", "Assigned"),
                    ("RESERVED", "Reserved"),
                    ("IN_TRANSIT", "In Transit"),
                    ("MAINTENANCE", "Under Preventive Maintenance"),
                    ("UNDER_REPAIR", "Under Repair"),
                    ("STOLEN", "Stolen"),
                    ("LOST", "Lost"),
                    ("RETIRED", "Retired"),
                    ("DISPOSED", "Disposed"),
                ],
                max_length=30,
            ),
        ),
    ]
