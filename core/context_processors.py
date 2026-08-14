from core.notifications.adapters import DjangoMessagesAdapter
from core.services.country_context import CountryContextService


def notifications(request):
    return {
        "notifications": DjangoMessagesAdapter.to_dtos(request),
    }


def country_context(request):

    if not request.user.is_authenticated:
        return {
            "country_context": None,
            "available_countries": [],
        }

    context = CountryContextService.resolve_request(
        request,
    )

    countries = CountryContextService.get_available_countries(
        request.user,
    )

    return {
        "country_context": context,
        "available_countries": countries,
    }