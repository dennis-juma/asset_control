from faker import Faker
from random import choice

from employees.models import Employee
from organizations.models import (
    Country,
    Department,
    JobTitle,
    Site,
)

fake = Faker()


class EmployeeSeeder:

    @staticmethod
    def run(stdout, total=30):
        country = Country.objects.first()

        departments = list(Department.objects.all())
        job_titles = list(JobTitle.objects.all())
        sites = list(Site.objects.all())

        if not all([country, departments, job_titles, sites]):
            stdout.write(
                "Please seed organizations before employees."
            )
            return

        created = 0

        for _ in range(total):

            first = fake.first_name()
            last = fake.last_name()

            email = f"{first.lower()}.{last.lower()}@sunking.com"

            if Employee.objects.filter(email=email).exists():
                continue

            Employee.objects.create(
                country=country,
                first_name=first,
                last_name=last,
                email=email,
                phone_number=fake.phone_number(),
                gender=choice(["M", "F"]),
                hire_date=fake.date_between(
                    start_date="-5y",
                    end_date="today",
                ),
                department=choice(departments),
                job_title=choice(job_titles),
                site=choice(sites),
            )

            created += 1

        stdout.write(
            "âœ” Employees seeded successfully."
        )