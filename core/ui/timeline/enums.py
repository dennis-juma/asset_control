from enum import Enum


class TimelineLevel(str, Enum):
    PRIMARY = "primary"
    SUCCESS = "success"
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"
    SECONDARY = "secondary"