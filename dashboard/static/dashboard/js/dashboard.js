document.addEventListener("DOMContentLoaded", () => {
    // Read chart data from the page
    // Create Chart.js instances
});

document.addEventListener("DOMContentLoaded", () => {

    const chartData = JSON.parse(
        document.getElementById("dashboard-chart-data").textContent
    );

    chartData.forEach(chart => {

        const canvas = document.getElementById(chart.chart_id);

        if (!canvas) {
            return;
        }

        new Chart(canvas, {
            type: chart.type,
            data: {
                labels: chart.labels,
                datasets: chart.datasets,
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
            }
        });

    });

});