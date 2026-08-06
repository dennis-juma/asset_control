from django.core.paginator import Paginator
from django.db.models import Q

from organizations.models import JobTitle


class JobTitleRepository:

    def list(
        self,
        query="",
        page=1,
        per_page=10,
    ):
        queryset = (
            JobTitle.objects
            .select_related(
                "company",
                "department",
            )
            .filter(
                is_deleted=False,
            )
            .order_by("name")
        )

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(code__icontains=query)
                | Q(company__name__icontains=query)
                | Q(department__name__icontains=query)
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
            JobTitle.objects
            .select_related(
                "company",
                "department",
            )
            .get(pk=pk)
        )

    def create(
        self,
        job_title,
    ):
        job_title.save()
        return job_title

    def update(
        self,
        job_title,
    ):
        job_title.save()
        return job_title

    def delete(
        self,
        job_title,
    ):
        job_title.delete()