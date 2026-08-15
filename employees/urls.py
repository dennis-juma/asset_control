from django.urls import path

from employees.views import (
    EmployeeCreateView,
    EmployeeDeleteView,
    EmployeeDetailView,
    EmployeeListView,
    EmployeeUpdateView,
    EmployeeBulkUpdateView,
)

app_name = "employees"

urlpatterns = [

    # =====================================================
    # Employee
    # =====================================================

    path(
        "",
        EmployeeListView.as_view(),
        name="employee-list",
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
]
