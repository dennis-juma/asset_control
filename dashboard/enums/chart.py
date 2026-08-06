from enum import StrEnum


class ChartType(StrEnum):
    BAR = "bar"
    LINE = "line"
    DOUGHNUT = "doughnut"
    PIE = "pie"
    POLAR_AREA = "polarArea"
    RADAR = "radar"