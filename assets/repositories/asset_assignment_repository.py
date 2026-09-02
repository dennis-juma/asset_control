from django.core.paginator import Paginator
from django.db.models import Q

from assets.choices.choices import AssignmentStatus
from assets.models import AssetAssignment


class AssetAssignmentRepository:

    def list(
        self,
        query="",
        page=1,
        per_page=20,
        country_context=None,
    ):

        queryset = (
            AssetAssignment.objects
            .select_related(
                "country",
                "asset",
                "asset__asset_model",
                "employee",
                "site",
            )
            .order_by("-assigned_date")
        )

        if country_context and country_context.country:
            queryset = queryset.filter(
                country=country_context.country,
            )

        if query:
            queryset = queryset.filter(
                Q(asset__asset_tag__icontains=query)
                | Q(asset__serial_number__icontains=query)
                | Q(employee__first_name__icontains=query)
                | Q(employee__last_name__icontains=query)
                | Q(site__name__icontains=query)
            )

        return Paginator(
            queryset,
            per_page,
        ).get_page(page)

    def export_queryset(
        self,
        query="",
        page=1,
        country_context=None,
    ):
        queryset = (
            AssetAssignment.objects
            .select_related(
                "country",
                "asset",
                "asset__asset_model",
                "employee",
                "site",
            )
            .order_by("-assigned_date")
        )

        if country_context and country_context.country:
            queryset = queryset.filter(
                country=country_context.country,
            )

        if query:
            queryset = queryset.filter(
                Q(asset__asset_tag__icontains=query)
                | Q(asset__serial_number__icontains=query)
                | Q(employee__first_name__icontains=query)
                | Q(employee__last_name__icontains=query)
                | Q(site__name__icontains=query)
            )

        return queryset

    def get(
        self,
        pk,
    ):
        return (
            AssetAssignment.objects
            .select_related(
                "country",
                "asset",
                "asset__asset_model",
                "employee",
                "site",
            )
            .get(pk=pk)
        )

    def create(
        self,
        assignment,
    ):
        assignment.save()
        return assignment

    def update(
        self,
        assignment,
    ):
        assignment.save()
        return assignment

    def active_assignment(
        self,
        asset,
    ):
        return (
            AssetAssignment.objects
            .filter(
                asset=asset,
                status=AssignmentStatus.ACTIVE,
            )
            .first()
        )

    def has_active_assignment(
        self,
        asset,
    ):

        return (
            AssetAssignment.objects
            .filter(
                asset=asset,
                status=AssignmentStatus.ACTIVE,
            )
            .exists()
        )

    def assignment_history(
        self,
        asset,
    ):

        return (
            AssetAssignment.objects
            .filter(
                asset=asset,
            )
            .order_by("-assigned_date")
        )
    def employee_active_assets(
    self,
    employee,
):
        return (
            AssetAssignment.objects
            .filter(
                employee=employee,
                status=AssignmentStatus.ACTIVE,
            )
            .select_related(
                "asset",
                "asset__asset_model",
            )
        )


    
