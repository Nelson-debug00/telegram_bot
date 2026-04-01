document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("pricesChart").getContext("2d");

    // historyData Debe estar definida globalmente en el HTML antes de cargar este script
    if (typeof historyData === "undefined") {
        console.error("historyData no está definida");
        return;
    }

    new Chart(ctx, {
        type: "line",
        data: {
            labels: historyData.labels,
            datasets: [
                {
                    label: "Dólar (BCV)",
                    data: historyData.dolar,
                    borderColor: "#19c3bd",
                    backgroundColor: "rgba(25, 195, 189, 0.1)",
                    borderWidth: 3,
                    tension: 0.3,
                    pointRadius: 5,
                    pointBackgroundColor: "#19c3bd",
                },
                {
                    label: "Euro (BCV)",
                    data: historyData.euro,
                    borderColor: "#ffcc00",
                    backgroundColor: "rgba(255, 204, 0, 0.1)",
                    borderWidth: 3,
                    tension: 0.3,
                    pointRadius: 5,
                    pointBackgroundColor: "#ffcc00",
                },
                {
                    label: "USDT (Paralelo)",
                    data: historyData.usdt,
                    borderColor: "#26a17b",
                    backgroundColor: "rgba(38, 161, 123, 0.1)",
                    borderWidth: 3,
                    tension: 0.3,
                    pointRadius: 5,
                    pointBackgroundColor: "#26a17b",
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: "top",
                    labels: {
                        color: "#ffffff",
                        font: { family: "Inter", size: 14 },
                    },
                },
                tooltip: {
                    mode: "index",
                    intersect: false,
                    backgroundColor: "#1a1f26",
                    titleColor: "#ffffff",
                    bodyColor: "#a1a1a1",
                    borderColor: "rgba(255, 255, 255, 0.1)",
                    borderWidth: 1,
                },
            },
            scales: {
                x: {
                    grid: { color: "rgba(255, 255, 255, 0.05)" },
                    ticks: { color: "#a1a1a1" },
                },
                y: {
                    grid: { color: "rgba(255, 255, 255, 0.05)" },
                    ticks: { color: "#a1a1a1" },
                    beginAtZero: false
                },
            },
        },
    });
});
