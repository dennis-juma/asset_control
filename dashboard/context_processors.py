from dashboard.services.navigation_service import NavigationService


def navigation(request):
    return {
        "navigation": NavigationService(request).get_navigation(),
    }