from enum import Enum


class WidgetType(str, Enum):
    STAT = "stat"
    CHART = "chart"
    TABLE = "table"
    ACTIVITY = "activity"
    ALERT = "alert"
    QUICK_ACTIONS = "quick_actions"