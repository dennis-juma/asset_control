from organizations.models import Company, JobTitle


class JobTitleSeeder:
    """
    Seeds company job titles.
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

        company = Company.objects.first()

        if not company:
            raise Exception(
                "No company found. Please run CompanySeeder first."
            )

        for title in JobTitleSeeder.JOB_TITLES:

            JobTitle.objects.get_or_create(
                company=company,
                name=title,
                defaults={
                    "description": title,
                },
            )

            stdout.write(f"  ✓ {title}")