import csv

from django.http import HttpResponse
from django.views import View

from employees.repositories import EmployeeRepository


class EmployeeExportView(View):

    def get(self, request):

        query = request.GET.get(
            "q",
            "",
        ).strip()

        repository = EmployeeRepository()

        page = repository.list(
            query=query,
            page=1,
            per_page=100000,
            country_context=getattr(
                request,
                "country_context",
                None,
            ),
        )

        response = HttpResponse(
            content_type="text/csv"
        )

        response["Content-Disposition"] = (
            'attachment; filename="employees.csv"'
        )

        writer = csv.writer(response)

        writer.writerow([
            "Employee ID",
            "Name",
            "Country",
            "Site",
            "Department",
            "Job Title",
            "Manager",
            "Gender",
            "Joining Date",
            "Last Working Date",
            "Phone",
            "Email",
            "Status",
        ])

        for employee in page:

            writer.writerow([
                employee.employee_id,
                employee.full_name,
                employee.country.name
                    if employee.country
                    else "",
                employee.site.name
                    if employee.site
                    else "",
                employee.department.name
                    if employee.department
                    else "",
                employee.job_title.name
                    if employee.job_title
                    else "",
                employee.manager.full_name
                    if employee.manager
                    else "",
                employee.get_gender_display(),
                employee.joining_date,
                employee.last_working_date
                    if employee.last_working_date
                    else "",
                employee.phone,
                employee.email,
                "Active"
                    if employee.is_active
                    else "Inactive",
            ])

        return response