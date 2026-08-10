import dashboard
from dashboard.services.statistics_service import StatisticsService
from dashboard.services.charts_service import ChartsService
from dashboard.services.trend_service import TrendService
from dashboard.serializers.chart_serializer import ChartSerializer
from dashboard.services.activities_service import ActivityService
from dashboard.services.alerts_service import AlertService
from dashboard.services.quick_actions_service import QuickActionService
from django.core.cache import cache
from dashboard.constants import (
    DASHBOARD_CACHE_KEY,
    DASHBOARD_CACHE_TIMEOUT,
)
from dashboard.services.system_health_service import (
    SystemHealthService,
)


class DashboardService:
    """
    Orchestrates all services required to build the dashboard.

    This service coordinates dashboard data without containing
    business logic. Individual dashboard sections are delegated
    to specialised services.
    """

    def __init__(self, request):
        self.request = request
        self.statistics_service = StatisticsService()
        self.charts_service = ChartsService()
        self.trend_service = TrendService()
        self.activity_service = ActivityService()
        self.alert_service = AlertService()
        self.quick_action_service = QuickActionService()
        self.system_health_service = SystemHealthService()
        
    
    def get_dashboard(self) -> dict:
        charts = self.charts_service.get_charts()
        trends = self.trend_service.get_trends()
        activity = self.activity_service.get_recent_activities()
        alert= self.alert_service.get_alerts()
        action = self.quick_action_service.get_actions()
        system_health = self.system_health_service.get_health()
        return {
            "statistics": self.statistics_service.get_cards(),
            "charts": charts,
            "trends": trends,
            "activity": activity,
            "alerts": alert,
            "quick_actions": action,
            "system_health": system_health,
            "chart_data": ChartSerializer.serialize(charts + trends),
        }