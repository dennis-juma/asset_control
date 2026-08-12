from organizations.models import Country, Department


class DepartmentSeeder:
    """
    Seeds country departments.
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

        country = Country.objects.first()

        if not country:
            raise Exception(
                "No country found. Please run CompanySeeder first."
            )

        departments = {}

        # Create parent departments first
        for name, parent_name in DepartmentSeeder.DEPARTMENTS:

            if parent_name is not None:
                continue

            department, created = Department.objects.get_or_create(
                country=country,
                name=name,
                defaults={
                    "description": f"{name} Department",
                },
            )

            departments[name] = department

            stdout.write(f"  âœ“ {name}")

        # Create child departments
        for name, parent_name in DepartmentSeeder.DEPARTMENTS:

            if parent_name is None:
                continue

            department, created = Department.objects.get_or_create(
                country=country,
                name=name,
                defaults={
                    "parent": departments[parent_name],
                    "description": f"{name} Department",
                },
            )

            departments[name] = department

            stdout.write(f"  âœ“ {name}")

        return departments