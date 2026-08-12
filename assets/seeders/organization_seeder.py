from assets.seeders.currency_seeder import CurrencySeeder
from assets.seeders.country_seeder import CountrySeeder
from assets.seeders.region_seeder import RegionSeeder
from assets.seeders.site_seeder import SiteSeeder
from assets.seeders.department_seeder import DepartmentSeeder
from assets.seeders.job_title_seeder import JobTitleSeeder


class SeederOrchestrator:
    """
    Coordinates the execution of all project seeders.
    """

    def __init__(self, command, options):
        self.command = command
        self.stdout = command.stdout
        self.style = command.style
        self.options = options

    def run(self):
        currencies = CurrencySeeder.run(self.stdout)

        countries = CountrySeeder.run(self.stdout)

        country = countries[0]

        regions = RegionSeeder.run(
            self.stdout,
            countries,
        )

        sites = SiteSeeder.run(
            self.stdout,
            regions,
        )

        departments = DepartmentSeeder.run(self.stdout)

        job_titles = JobTitleSeeder.run(self.stdout)

        return {
            "country": country,
            "currencies": currencies,
            "countries": countries,
            "regions": regions,
            "sites": sites,
            "departments": departments,
            "job_titles": job_titles,
            
        }
