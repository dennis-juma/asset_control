from organizations.models import Country


class CountrySeeder:

    DEFAULT_COUNTRIES = [
        {
            "name": "Tanzania",
            "iso2": "TZ",
            "iso3": "TZA",
            "currency": "TZS",
            "timezone": "Africa/Dar_es_Salaam",
            "phone_code": "+255",
        },
        {
            "name": "Kenya",
            "iso2": "KE",
            "iso3": "KEN",
            "currency": "KES",
            "timezone": "Africa/Nairobi",
            "phone_code": "+254",
        },
    ]

    @classmethod
    def run(cls, stdout):

        countries = []

        stdout.write("Creating countries...")

        for data in cls.DEFAULT_COUNTRIES:

            country, created = Country.objects.get_or_create(
                iso2=data["iso2"],
                defaults=data,
            )

            countries.append(country)

            if created:
                stdout.write(f"  ✓ {country.name}")
            else:
                stdout.write(f"  • {country.name} already exists")

        return countries
