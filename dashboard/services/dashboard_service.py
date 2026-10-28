from core.services.country_context import CountryContextService

from dashboard.serializers.chart_serializer import ChartSerializer
from dashboard.services.statistics_service import StatisticsService
from dashboard.services.charts_service import ChartsService
from dashboard.services.trend_service import TrendService
from dashboard.services.activities_service import ActivityService
from dashboard.services.alerts_service import AlertService
from dashboard.services.quick_actions_service import QuickActionService
from dashboard.services.system_health_service import SystemHealthService


class DashboardService:

    def __init__(self, request):

        self.request = request

        self.country_context = (
            CountryContextService.resolve_request(
                request,
            )
        )

        country = self.country_context.country

        self.statistics = StatisticsService(
            country=country,
        )

        self.charts = ChartsService(
            country=country,
        )

        self.trends = TrendService(
            country=country,
        )

        self.activities = ActivityService(
            country=country,
        )

        self.alerts = AlertService(
            country=country,
        )

        self.quick_actions = QuickActionService()

        self.system_health = SystemHealthService()

    def get_dashboard(self):

        charts = self.charts.get_charts()
        trends = self.trends.get_trends()
        chart_data = charts + trends

        return {
            "statistics": self.statistics.get_cards(),
            "charts": charts,
            "trends": trends,
            "chart_data": ChartSerializer.serialize(chart_data),
            "activities": self.activities.get_recent_activities(),
            "alerts": self.alerts.get_alerts(),
            "quick_actions": self.quick_actions.get_actions(),
            "system_health": self.system_health.get_health(),
            "country_context": self.country_context,
        }
