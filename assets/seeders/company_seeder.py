from organizations.models import Company


class CompanySeeder:
    """
    Seeds the default company.
    """

    @staticmethod
    def run(stdout):
        company, created = Company.objects.get_or_create(
            name="Sun King Tanzania Ltd",
            defaults={
                "legal_name": "Sun King Tanzania Limited",
                "registration_number": "REG-001",
                "tax_number": "TIN-001",
                "email": "info@sunking.com",
                "phone": "+255700000000",
                "website": "https://www.sunking.com",
                "description": "Default demo company.",
            },
        )

        if created:
            stdout.write(
                "✔ Company created"
            )
        else:
            stdout.write(
                "✔ Company already exists"
            )

        return company