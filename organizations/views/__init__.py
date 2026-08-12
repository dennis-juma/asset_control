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
