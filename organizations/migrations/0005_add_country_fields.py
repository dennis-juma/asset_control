import django.db.models.deletion
from django.db import migrations, models


def copy_company_country(apps, schema_editor):
    Company = apps.get_model("organizations", "Company")
    Department = apps.get_model("organizations", "Department")
    JobTitle = apps.get_model("organizations", "JobTitle")

    company_countries = dict(
        Company.objects.values_list("id", "country_id")
    )
    for model in (Department, JobTitle):
        for record in model.objects.exclude(company_id=None):
            record.country_id = company_countries[record.company_id]
            record.save(update_fields=["country"])


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0004_alter_jobtitle_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="department",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="departments",
                to="organizations.country",
            ),
        ),
        migrations.AddField(
            model_name="jobtitle",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="job_titles",
                to="organizations.country",
            ),
        ),
        migrations.RunPython(copy_company_country, migrations.RunPython.noop),
    ]
