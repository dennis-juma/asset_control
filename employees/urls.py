from django.urls import path
from employees.views.employee_export import EmployeeExportView
from employees.views.employee_import import EmployeeImportView
from .views.employee_profile import employee_profile
from .views.employee_asset_detail import employee_asset_detail

from employees.views import (
    EmployeeCreateView,
    EmployeeDeleteView,
    EmployeeDetailView,
    EmployeeListView,
    EmployeeUpdateView,
    EmployeeBulkUpdateView,
)
from employees.views.employee_autocomplete import EmployeeAutocompleteView

app_name = "employees"

urlpatterns = [

    # =====================================================
    # Employee
    # =====================================================

    path(
    "my-profile/",
    employee_profile,
    name="my-profile",
),
path(
    "my-assets/<uuid:asset_pk>/",
    employee_asset_detail,
    name="my-asset-detail",
),

    path(
        "",
        EmployeeListView.as_view(),
        name="employee-list",
    ),
    path(
        "autocomplete/",
        # remote autocomplete for tom-select
        EmployeeAutocompleteView.as_view(),
        name="employee-autocomplete",
    ),

    path(
        "create/",
        EmployeeCreateView.as_view(),
        name="employee-create",
    ),

    path(
        "bulk-update/",
        EmployeeBulkUpdateView.as_view(),
        name="employee-bulk-update",
    ),
    path(
    "import/",
    EmployeeImportView.as_view(),
    name="employee-import",
    ),

    path(
        "<uuid:pk>/",
        EmployeeDetailView.as_view(),
        name="employee-detail",
    ),

    path(
        "<uuid:pk>/edit/",
        EmployeeUpdateView.as_view(),
        name="employee-update",
    ),

    path(
        "<uuid:pk>/delete/",
        EmployeeDeleteView.as_view(),
        name="employee-delete",
    ),
    path(
    "export/",
    EmployeeExportView.as_view(),
    name="employee-export",
),
]
