from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ChartOptions:
    """
    Presentation options for dashboard charts.
    """

    responsive: bool = True

    maintain_aspect_ratio: bool = False

    show_legend: bool = True

    show_title: bool = False

    stacked: bool = False