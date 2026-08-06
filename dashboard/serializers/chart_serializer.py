from dashboard.dto.chart_data import ChartData


class ChartSerializer:
    """
    Serialize ChartData DTOs for Chart.js.
    """

    @staticmethod
    def serialize(charts: list[ChartData]) -> list[dict]:
        return [
            {
                "chart_id": chart.chart_id,
                "title": chart.title,
                "type": chart.chart_type.value,
                "labels": chart.labels,
                "datasets": [
                    {
                        "label": dataset.label,
                        "data": dataset.data,
                        "backgroundColor": dataset.background_color,
                        "borderColor": dataset.border_color,
                        "borderWidth": dataset.border_width,
                        "fill": dataset.fill,
                        "tension": dataset.tension,
                    }
                    for dataset in chart.datasets
                ],
            }
            for chart in charts
        ]