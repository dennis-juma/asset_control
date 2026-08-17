from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from assets.choices import AssignmentStatus
from assets.models import AssetAssignment


@login_required
def employee_asset_detail(request, asset_pk):

    employee = getattr(
        request.user,
        "employee",
        None,
    )

    if employee is None:
        return render(
            request,
            "employees/asset_detail.html",
            {
                "employee": None,
                "assignment": None,
                "asset": None,
                "history": [],
            },
        )

    assignment = get_object_or_404(
        AssetAssignment.objects.select_related(
            "asset",
            "asset__asset_model",
            "asset__asset_model__brand",
            "employee",
            "site",
        ),
        asset_id=asset_pk,
        employee=employee,
        status=AssignmentStatus.ACTIVE,
    )

    asset = assignment.asset

    history = (
        asset.history
        .select_related(
            "employee",
            "site",
            "performed_by",
        )
        .order_by("-event_date")
    )

    return render(
        request,
        "employees/asset_detail.html",
        {
            "employee": employee,
            "assignment": assignment,
            "asset": asset,
            "history": history,
        },
    )