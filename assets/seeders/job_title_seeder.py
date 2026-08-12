from organizations.models import Country, JobTitle


class JobTitleSeeder:
    """
    Seeds country job titles.
    """

    JOB_TITLES = [
        "IT Manager",
        "Senior IT Associate",
        "IT Support Engineer",
        "System Administrator",
        "Network Engineer",
        "Finance Manager",
        "Finance Officer",
        "Accountant",
        "HR Manager",
        "HR Officer",
        "Operations Manager",
        "Regional Business Manager",
        "Supervisor",
        "Call Center Manager",
        "Call Center Agent",
        "Warehouse Manager",
        "Warehouse Officer",
        "Inventory Officer",
        "Procurement Officer",
        "Area Business Manager",
        "Sales Officer",
        "Marketing Manager",
        "Marketing Officer",
        "Field Technician",
    ]

    @staticmethod
    def run(stdout):
        stdout.write("Creating job titles...")

        country = Country.objects.first()

        if not country:
            raise Exception(
                "No country found. Please run CompanySeeder first."
            )

        for title in JobTitleSeeder.JOB_TITLES:

            JobTitle.objects.get_or_create(
                country=country,
                name=title,
                defaults={
                    "description": title,
                },
            )

            stdout.write(f"  âœ“ {title}")