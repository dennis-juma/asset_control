from django.core.paginator import Paginator
from django.db.models import Q

from employees.models import Employee


class EmployeeRepository:

    def list(
        self,
        query="",
        page=1,
        per_page=10,
    ):
        queryset = (
            Employee.objects
            .select_related(
                "country",
                "site",
                "department",
                "job_title",
                "manager",
                "user",
            )
            .order_by(
                "first_name",
                "last_name",
            )
        )

        if query:

            queryset = queryset.filter(

                Q(employee_id__icontains=query)
                | Q(first_name__icontains=query)
                | Q(middle_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(email__icontains=query)
                | Q(phone__icontains=query)
                | Q(country__name__icontains=query)
                | Q(site__name__icontains=query)
                | Q(department__name__icontains=query)
                | Q(job_title__name__icontains=query)

            )

        paginator = Paginator(
            queryset,
            per_page,
        )

        return paginator.get_page(page)

    def get(
        self,
        pk,
    ):
        return (
            Employee.objects
            .select_related(
                "country",
                "site",
                "department",
                "job_title",
                "manager",
                "user",
            )
            .get(
                pk=pk,
            )
        )

    def create(
        self,
        employee,
    ):
        employee.save()

        return employee

    def update(
        self,
        employee,
    ):
        employee.save()

        return employee

    def delete(
        self,
        employee,
    ):
        employee.delete()