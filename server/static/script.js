let methaneChart = null;
let riskChart = null;
let gauge = null;
let previousRisk = null;

function logToTerminal(message) {
    const terminal = document.getElementById("aiTerminal");
    if (!terminal) return;

    const line = document.createElement("div");
    line.classList.add("terminal-line");

    const time = new Date().toLocaleTimeString();
    line.innerText = `[AI ${time}] ${message}`;

    terminal.appendChild(line);
    terminal.scrollTop = terminal.scrollHeight;
}

function getGaugeColor(risk) {
    if (risk < 120) return "#00ff88";
    if (risk < 200) return "#ffaa00";
    return "#ff0066";
}

function getRiskLevel(risk) {
    if (risk > 300) return "CRITICAL";
    if (risk > 200) return "DANGER";
    if (risk > 120) return "CAUTION";
    return "SAFE";
}

function createCharts(data) {

    const labels = data.timestamps.slice(-30).map(t =>
        new Date(t).toLocaleTimeString()
    );

    const methane = data.methane.slice(-30);
    const risk = data.risk.slice(-30);

    const latestRisk = risk.length ? risk[risk.length - 1] : 0;
    previousRisk = latestRisk;

    methaneChart = new Chart(document.getElementById("methaneChart"), {
        type: "line",
        data: {
            labels,
            datasets: [{
                label: "Methane",
                data: methane,
                borderColor: "#00ffff",
                backgroundColor: "rgba(0,255,255,0.15)",
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: "#00ffff" } }
            },
            scales: {
                x: { ticks: { color: "#00ffff" } },
                y: { ticks: { color: "#00ffff" } }
            }
        }
    });

    riskChart = new Chart(document.getElementById("riskChart"), {
        type: "line",
        data: {
            labels,
            datasets: [{
                label: "Risk Score",
                data: risk,
                borderColor: "#ff00ff",
                backgroundColor: "rgba(255,0,255,0.15)",
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: "#ff00ff" } }
            },
            scales: {
                x: { ticks: { color: "#ff00ff" } },
                y: { ticks: { color: "#ff00ff" } }
            }
        }
    });

    gauge = new Chart(document.getElementById("riskGauge"), {
        type: "doughnut",
        data: {
            datasets: [{
                data: [latestRisk, 500 - latestRisk],
                backgroundColor: [getGaugeColor(latestRisk), "#111"],
                borderWidth: 0
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            rotation: -90,
            circumference: 180,
            plugins: { legend: { display: false } }
        }
    });

    logToTerminal("Neural monitoring initialized.");
    updateMineGrid(data);
}

function updateCharts(data) {

    const labels = data.timestamps.slice(-30).map(t =>
        new Date(t).toLocaleTimeString()
    );

    const methane = data.methane.slice(-30);
    const risk = data.risk.slice(-30);

    const latestRisk = risk.length ? risk[risk.length - 1] : 0;

    methaneChart.data.labels = labels;
    methaneChart.data.datasets[0].data = methane;
    methaneChart.update();

    riskChart.data.labels = labels;
    riskChart.data.datasets[0].data = risk;
    riskChart.update();

    gauge.data.datasets[0].data = [
        latestRisk,
        500 - latestRisk
    ];
    gauge.data.datasets[0].backgroundColor[0] =
        getGaugeColor(latestRisk);
    gauge.update();

    // AI Spike Detection
    if (previousRisk !== null && latestRisk - previousRisk > 40) {
        logToTerminal("⚠ Risk spike detected.");
        document.body.classList.add("flash-alert");
        setTimeout(() =>
            document.body.classList.remove("flash-alert"),
            500
        );
    }

    previousRisk = latestRisk;

    updateMineGrid(data);
}

function updateMineGrid(data) {

    const grid = document.getElementById("mineGrid");
    if (!grid) return;

    grid.innerHTML = "";

    const latestRisk = data.risk[data.risk.length - 1] || 0;
    const level = getRiskLevel(latestRisk);

    for (let i = 1; i <= 9; i++) {

        const node = document.createElement("div");
        node.classList.add("mine-node");

        node.classList.add(level.toLowerCase());

        node.innerHTML = `
            <div>
                Node ${i}<br>
                <strong>${level}</strong>
            </div>
        `;

        grid.appendChild(node);
    }
}

function fetchData() {

    fetch("/analytics")
        .then(res => res.json())
        .then(data => {
            if (!methaneChart) createCharts(data);
            else updateCharts(data);
        });

    fetch("/stats")
        .then(res => res.json())
        .then(stats => {
            const total = document.getElementById("totalPackets");
            const emergency = document.getElementById("emergencyCount");

            if (total) total.innerText = stats.total_packets;
            if (emergency) emergency.innerText = stats.emergency_count;
        });
}

setInterval(fetchData, 4000);
fetchData();