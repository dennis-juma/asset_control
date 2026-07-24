from sys import stdout

from django.core.management.base import BaseCommand
from faker import Faker
from assets.seeders.orchestrator import SeederOrchestrator
from employees.seeders.employee_seeder import EmployeeSeeder


class Command(BaseCommand):
    help = "Seed demo data for Asset Management System"

    def add_arguments(self, parser):
        parser.add_argument(
            "--assets",
            type=int,
            default=100,
            help="Number of assets to create.",
        )

        parser.add_argument(
            "--employees",
            type=int,
            default=20,
            help="Number of employees to create.",
        )

        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete demo data before seeding.",
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                "===================================="
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                " Asset Management Seeder"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "===================================="
            )
        )

        self.stdout.write(f"Assets     : {options['assets']}")
        self.stdout.write(f"Employees  : {options['employees']}")
        self.stdout.write(f"Reset      : {options['reset']}")

        SeederOrchestrator(
    command=self,
    options=options,
).run()
        

    stdout.write("Creating employees...")
    EmployeeSeeder.run(stdout)