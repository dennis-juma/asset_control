__all__ = [
    "BreadcrumbDTO",
    "PageDTO",
]


def __getattr__(name):
    if name == "BreadcrumbDTO":
        from core.dtos import BreadcrumbDTO
        return BreadcrumbDTO
    if name == "PageDTO":
        from core.dtos import PageDTO
        return PageDTO
    raise AttributeError(
        f"module {__name__!r} has no attribute {name!r}"
    )