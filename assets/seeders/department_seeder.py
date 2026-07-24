from organizations.models import Company, Department


class DepartmentSeeder:
    """
    Seeds company departments.
    """

    DEPARTMENTS = [
        ("Executive", None),
        ("Information Technology", None),
        ("Finance", None),
        ("Human Resources", None),
        ("Operations", None),
        ("Sales", None),
        ("Marketing", None),
        ("Customer Experience", None),
        ("Supply Chain", None),
        ("Procurement", None),
        ("Engineering", None),
        ("Legal", None),
        ("Field Operations", "Operations"),
        ("Warehouse", "Supply Chain"),
    ]

    @staticmethod
    def run(stdout):
        stdout.write("Creating departments...")

        company = Company.objects.first()

        if not company:
            raise Exception(
                "No company found. Please run CompanySeeder first."
            )

        departments = {}

        # Create parent departments first
        for name, parent_name in DepartmentSeeder.DEPARTMENTS:

            if parent_name is not None:
                continue

            department, created = Department.objects.get_or_create(
                company=company,
                name=name,
                defaults={
                    "description": f"{name} Department",
                },
            )

            departments[name] = department

            stdout.write(f"  ✓ {name}")

        # Create child departments
        for name, parent_name in DepartmentSeeder.DEPARTMENTS:

            if parent_name is None:
                continue

            department, created = Department.objects.get_or_create(
                company=company,
                name=name,
                defaults={
                    "parent": departments[parent_name],
                    "description": f"{name} Department",
                },
            )

            departments[name] = department

            stdout.write(f"  ✓ {name}")

        return departments