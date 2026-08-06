from .company import (
    CompanyCreateView,
    CompanyDetailView,
    CompanyListView,
    CompanyUpdateView,
)
from .country import (
    CountryListView,
    CountryCreateView,
    CountryDetailView,
    CountryUpdateView,
    CountryDeleteView,
)

from .site import (
    SiteListView,
    SiteCreateView,
    SiteDetailView,
    SiteUpdateView,
    SiteDeleteView,
)
from .job_title import (
    JobTitleListView,
    JobTitleCreateView,
    JobTitleDetailView,
    JobTitleUpdateView,
    JobTitleDeleteView,
)

__all__ = [
    "CompanyListView",
    "CompanyCreateView",
    "CompanyDetailView",
    "CompanyUpdateView",

    "CountryListView",
    "CountryCreateView",
    "CountryDetailView",
    "CountryUpdateView",
    "CountryDeleteView",


    "SiteListView",
    "SiteCreateView",
    "SiteDetailView",
    "SiteUpdateView",
    "SiteDeleteView",

    "JobTitleListView",
    "JobTitleCreateView",
    "JobTitleDetailView",
    "JobTitleUpdateView",
    "JobTitleDeleteView",
]