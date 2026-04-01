document.addEventListener("DOMContentLoaded", function () {
    // historyData Debe estar definida globalmente en el HTML
    if (typeof historyData === "undefined") {
        console.error("historyData no está definida");
        return;
    }

    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                mode: "index",
                intersect: false,
                backgroundColor: "#1a1f26",
                titleColor: "#ffffff",
                bodyColor: "#a1a1a1",
                borderColor: "rgba(255, 255, 255, 0.1)",
                borderWidth: 1,
                padding: 12,
                displayColors: false,
            },
        },
        scales: {
            x: {
                grid: { display: false },
                ticks: { color: "#a1a1a1", font: { size: 11 } },
            },
            y: {
                grid: { color: "rgba(255, 255, 255, 0.05)" },
                ticks: { color: "#a1a1a1", font: { size: 11 } },
                beginAtZero: false,
            },
        },
    };

    const createGradient = (ctx, color) => {
        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, color.replace("1)", "0.3)"));
        gradient.addColorStop(1, color.replace("1)", "0)"));
        return gradient;
    };

    // --- Gráfico Dólar ---
    const ctxDolar = document.getElementById("dolarChart").getContext("2d");
    new Chart(ctxDolar, {
        type: "line",
        data: {
            labels: historyData.labels,
            datasets: [
                {
                    label: "Dólar BCV",
                    data: historyData.dolar,
                    borderColor: "#19c3bd",
                    backgroundColor: createGradient(ctxDolar, "rgba(25, 195, 189, 1)"),
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: "#19c3bd",
                    pointHoverRadius: 6,
                },
            ],
        },
        options: commonOptions,
    });

    // --- Gráfico Euro ---
    const ctxEuro = document.getElementById("euroChart").getContext("2d");
    new Chart(ctxEuro, {
        type: "line",
        data: {
            labels: historyData.labels,
            datasets: [
                {
                    label: "Euro BCV",
                    data: historyData.euro,
                    borderColor: "#ffcc00",
                    backgroundColor: createGradient(ctxEuro, "rgba(255, 204, 0, 1)"),
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: "#ffcc00",
                    pointHoverRadius: 6,
                },
            ],
        },
        options: commonOptions,
    });

    // --- Gráfico USDT ---
    const ctxUsdt = document.getElementById("usdtChart").getContext("2d");
    new Chart(ctxUsdt, {
        type: "line",
        data: {
            labels: historyData.labels,
            datasets: [
                {
                    label: "USDT Paralelo",
                    data: historyData.usdt,
                    borderColor: "#26a17b",
                    backgroundColor: createGradient(ctxUsdt, "rgba(38, 161, 123, 1)"),
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: "#26a17b",
                    pointHoverRadius: 6,
                },
            ],
        },
        options: commonOptions,
    });
});
