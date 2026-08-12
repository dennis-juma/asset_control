from django.views.generic import TemplateView

from core.permissions.mixins import PermissionRequiredMixin
from dashboard.services.dashboard_service import DashboardService


class DashboardView(PermissionRequiredMixin, TemplateView):
    """
    Display the main dashboard.

    Business logic is delegated to DashboardService,
    keeping the view thin and focused on HTTP handling.
    """

    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        dashboard_service = DashboardService(self.request)
        context.update(dashboard_service.get_dashboard())

        return context
