from organizations.models import Region


class RegionSeeder:

    DEFAULT_REGIONS = {
        "Tanzania": [
            "Arusha",
            "Dar es Salaam",
            "Dodoma",
            "Mwanza",
        ],
        "Kenya": [
            "Nairobi",
            "Mombasa",
        ],
    }

    @classmethod
    def run(cls, stdout, countries):

        regions = []

        stdout.write("Creating regions...")

        for country in countries:

            for region_name in cls.DEFAULT_REGIONS.get(country.name, []):

                region, created = Region.objects.get_or_create(
                    country=country,
                    name=region_name,
                )

                regions.append(region)

                if created:
                    stdout.write(f"  ✓ {region.name}")
                else:
                    stdout.write(f"  • {region.name} already exists")

        return regions