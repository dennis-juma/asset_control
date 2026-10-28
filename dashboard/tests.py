from unittest.mock import Mock, patch

from django.test import RequestFactory, SimpleTestCase
from django.contrib.auth.models import AnonymousUser

from dashboard.services.dashboard_service import DashboardService


class DashboardServiceTests(SimpleTestCase):

	@patch("dashboard.services.dashboard_service.SystemHealthService")
	@patch("dashboard.services.dashboard_service.QuickActionService")
	@patch("dashboard.services.dashboard_service.AlertService")
	@patch("dashboard.services.dashboard_service.ActivityService")
	@patch("dashboard.services.dashboard_service.TrendService")
	@patch("dashboard.services.dashboard_service.ChartsService")
	@patch("dashboard.services.dashboard_service.StatisticsService")
	def test_dashboard_builds_charts_and_trends_once(
		self,
		statistics_service,
		charts_service,
		trend_service,
		activity_service,
		alert_service,
		quick_action_service,
		system_health_service,
	):
		request = RequestFactory().get("/")
		request.user = AnonymousUser()

		charts = []
		trends = []
		charts_service.return_value.get_charts.return_value = charts
		trend_service.return_value.get_trends.return_value = trends

		DashboardService(request).get_dashboard()

		charts_service.return_value.get_charts.assert_called_once_with()
		trend_service.return_value.get_trends.assert_called_once_with()
