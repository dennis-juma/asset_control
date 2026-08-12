from common.choices import SiteType
from organizations.models import Site


class SiteSeeder:
    """
    Seeds default country sites.
    """

    DEFAULT_SITES = {
        "Arusha": [
            {
                "name": "Arusha Head Office",
                "site_type": SiteType.HEAD_OFFICE,
                "city": "Arusha",
            },
            {
                "name": "Arusha Warehouse",
                "site_type": SiteType.WAREHOUSE,
                "city": "Arusha",
            },
        ],
        "Dar es Salaam": [
            {
                "name": "Dar Regional Office",
                "site_type": SiteType.REGIONAL_OFFICE,
                "city": "Dar es Salaam",
            },
            {
                "name": "Dar Call Center",
                "site_type": SiteType.CALL_CENTER,
                "city": "Dar es Salaam",
            },
        ],
        "Dodoma": [
            {
                "name": "Dodoma Field Base",
                "site_type": SiteType.FIELD_BASE,
                "city": "Dodoma",
            },
        ],
        "Mwanza": [
            {
                "name": "Mwanza Service Center",
                "site_type": SiteType.SERVICE_CENTER,
                "city": "Mwanza",
            },
        ],
        "Nairobi": [
            {
                "name": "Nairobi Regional Office",
                "site_type": SiteType.REGIONAL_OFFICE,
                "city": "Nairobi",
            },
        ],
        "Mombasa": [
            {
                "name": "Mombasa Warehouse",
                "site_type": SiteType.WAREHOUSE,
                "city": "Mombasa",
            },
        ],
    }

    @classmethod
    def run(cls, stdout, regions):
        sites = []

        stdout.write("Creating sites...")

        for region in regions:

            region_sites = cls.DEFAULT_SITES.get(region.name, [])

            for data in region_sites:

                site, created = Site.objects.get_or_create(
                    region=region,
                    name=data["name"],
                    defaults={
                        "site_type": data["site_type"],
                        "city": data["city"],
                    },
                )

                sites.append(site)

                if created:
                    stdout.write(f"  âœ“ {site.name}")
                else:
                    stdout.write(f"  â€¢ {site.name} already exists")

        return sites