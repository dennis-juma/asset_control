from django.urls import path

from organizations.views.country import (
    CompanyCreateView,
    CompanyDeleteView,
    CompanyDetailView,
    CompanyListView,
    CompanyUpdateView,
)
from organizations.views import (
    CountryListView,
    CountryCreateView,
    CountryDetailView,
    CountryUpdateView,
    CountryDeleteView,
)
from organizations.views import (
    SiteListView,
    SiteCreateView,
    SiteDetailView,
    SiteUpdateView,
    SiteDeleteView,
)

from organizations.views.department import (
    DepartmentCreateView,
    DepartmentDeleteView,
    DepartmentDetailView,
    DepartmentListView,
    DepartmentUpdateView,
)

from organizations.views.job_title import (
    JobTitleListView,
    JobTitleCreateView,
    JobTitleDetailView,
    JobTitleUpdateView,
    JobTitleDeleteView,
)


app_name = "organizations"

urlpatterns = [

    # Country
    path(
        "companies/",
        CompanyListView.as_view(),
        name="country-list",
    ),

    path(
        "companies/create/",
        CompanyCreateView.as_view(),
        name="country-create",
    ),

    path(
        "companies/<uuid:pk>/",
        CompanyDetailView.as_view(),
        name="country-detail",
    ),

    path(
        "companies/<uuid:pk>/edit/",
        CompanyUpdateView.as_view(),
        name="country-edit",
    ),
    path(
        "companies/<uuid:pk>/delete/",
        CompanyDeleteView.as_view(),
        name="country-delete",
    ),

    # Countries

path(
    "countries/",
    CountryListView.as_view(),
    name="country-list",
),

path(
    "countries/create/",
    CountryCreateView.as_view(),
    name="country-create",
),

path(
    "countries/<uuid:pk>/",
    CountryDetailView.as_view(),
    name="country-detail",
),

path(
    "countries/<uuid:pk>/edit/",
    CountryUpdateView.as_view(),
    name="country-update",
),

path(
    "countries/<uuid:pk>/delete/",
    CountryDeleteView.as_view(),
    name="country-delete",
),

path(
    "sites/",
    SiteListView.as_view(),
    name="site-list",
),

path(
    "sites/create/",
    SiteCreateView.as_view(),
    name="site-create",
),

path(
    "sites/<uuid:pk>/",
    SiteDetailView.as_view(),
    name="site-detail",
),

path(
    "sites/<uuid:pk>/edit/",
    SiteUpdateView.as_view(),
    name="site-update",
),

path(
    "sites/<uuid:pk>/delete/",
    SiteDeleteView.as_view(),
    name="site-delete",
),

path(
        "departments/",
        DepartmentListView.as_view(),
        name="department-list",
    ),
    path(
        "departments/create/",
        DepartmentCreateView.as_view(),
        name="department-create",
    ),
    path(
        "departments/<uuid:pk>/",
        DepartmentDetailView.as_view(),
        name="department-detail",
    ),
    path(
        "departments/<uuid:pk>/edit/",
        DepartmentUpdateView.as_view(),
        name="department-update",
    ),
    path(
        "departments/<uuid:pk>/delete/",
        DepartmentDeleteView.as_view(),
        name="department-delete",
    ),
    # ==========================================
# Job Titles
# ==========================================

path(
    "job-titles/",
    JobTitleListView.as_view(),
    name="job-title-list",
),

path(
    "job-titles/create/",
    JobTitleCreateView.as_view(),
    name="job-title-create",
),

path(
    "job-titles/<uuid:pk>/",
    JobTitleDetailView.as_view(),
    name="job-title-detail",
),

path(
    "job-titles/<uuid:pk>/edit/",
    JobTitleUpdateView.as_view(),
    name="job-title-update",
),

path(
    "job-titles/<uuid:pk>/delete/",
    JobTitleDeleteView.as_view(),
    name="job-title-delete",
),
    


]
