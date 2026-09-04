from django.core.paginator import Paginator
from django.db.models import Q

from employees.models import Employee


class EmployeeRepository:

    def list(
        self,
        query="",
        page=1,
        per_page=10,
        country_context=None,
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

        if country_context and country_context.country:
            queryset = queryset.filter(
                country=country_context.country,
            )

        if query:
            # Tokenized name search: allow searching "First Last" or partial terms
            terms = [t.strip() for t in str(query).split() if t.strip()]

            # start with broad OR across identifier fields
            combined = (
                Q(employee_id__icontains=query)
                | Q(email__icontains=query)
                | Q(phone__icontains=query)
                | Q(country__name__icontains=query)
                | Q(site__name__icontains=query)
                | Q(department__name__icontains=query)
                | Q(job_title__name__icontains=query)
            )

            # For each token, require it to match either first/middle/last name
            for term in terms:
                name_q = (
                    Q(first_name__icontains=term)
                    | Q(middle_name__icontains=term)
                    | Q(last_name__icontains=term)
                )
                combined = combined | name_q

            queryset = queryset.filter(combined)

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
