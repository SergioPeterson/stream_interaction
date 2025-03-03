import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from "chart.js";
import { Line } from "react-chartjs-2";

// ✅ Register required Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function ViewerChart({ viewerData, selectedSession }) {
    if (!selectedSession || !viewerData[selectedSession]) return null;

    const sessionData = viewerData[selectedSession];

    const data = {
        labels: sessionData.map((d) => d.minute),
        datasets: [
            {
                label: "Viewers Over Time",
                data: sessionData.map((d) => d.viewer_count),
                borderColor: "blue",
                backgroundColor: "rgba(0, 0, 255, 0.5)",
                fill: false,
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                display: true,
            },
            title: {
                display: true,
                text: "Viewer Count Over Time",
            },
        },
        scales: {
            x: {
                type: "category",
                title: {
                    display: true,
                    text: "Time (minutes)",
                },
            },
            y: {
                type: "linear",
                title: {
                    display: true,
                    text: "Viewer Count",
                },
            },
        },
    };

    return <Line data={data} options={options} />;
}