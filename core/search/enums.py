from enum import Enum


class SearchScope(str, Enum):

    GLOBAL = "global"

    MODULE = "module"

    QUICK = "quick"


class SearchResultType(str, Enum):

    ASSET = "asset"

    EMPLOYEE = "employee"

    COMPANY = "company"

    LOCATION = "location"

    VENDOR = "vendor"