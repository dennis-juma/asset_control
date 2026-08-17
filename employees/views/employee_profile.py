from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from assets.choices import AssignmentStatus
from assets.models import AssetAssignment


@login_required
def employee_profile(request):

    employee = getattr(
        request.user,
        "employee",
        None,
    )

    if employee is None:
        return render(
            request,
            "employees/profile.html",
            {
                "employee": None,
                "assigned_assets": [],
            },
        )

    assigned_assets = (
        AssetAssignment.objects
        .filter(
            employee=employee,
            status=AssignmentStatus.ACTIVE,
        )
        .select_related(
            "asset",
            "asset__asset_model",
            "asset__asset_model__brand",
        )
        .order_by(
            "asset__asset_tag",
        )
    )

    return render(
        request,
        "employees/profile.html",
        {
            "employee": employee,
            "assigned_assets": assigned_assets,
        },
    )