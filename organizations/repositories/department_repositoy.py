from django.core.paginator import Paginator
from django.db.models import Q

from organizations.models import Department


class DepartmentRepository:

    def list(
        self,
        query="",
        page=1,
        per_page=20,
    ):
        queryset = (
            Department.objects
            .select_related(
                "country",
                "site",
                "parent",
            )
            .filter(
                is_deleted=False,
            )
        )

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(code__icontains=query)
                | Q(cost_center__icontains=query)
                | Q(country__name__icontains=query)
                | Q(site__name__icontains=query)
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
            Department.objects
            .select_related(
                "country",
                "site",
                "parent",
            )
            .get(pk=pk)
        )