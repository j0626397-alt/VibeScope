import { useEffect, useRef } from "react";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const EMOTION_CONFIG = {
  happy: { color: "#43e8a4", icon: "😊" },
  excitement: { color: "#fbbf24", icon: "⚡" },
  neutral: { color: "#6c63ff", icon: "😐" },
  sadness: { color: "#818cf8", icon: "😔" },
  anger: { color: "#ff6584", icon: "😠" },
};

export default function EmotionChart({ data }) {
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current || !data) return;

    if (chartRef.current) chartRef.current.destroy();

    const emotions = Object.keys(data);
    const values = Object.values(data);
    const colors = emotions.map((e) => EMOTION_CONFIG[e]?.color || "#6c63ff");

    chartRef.current = new Chart(canvasRef.current, {
      type: "polarArea",
      data: {
        labels: emotions.map(
          (e) => `${EMOTION_CONFIG[e]?.icon || ""} ${e.charAt(0).toUpperCase() + e.slice(1)}`
        ),
        datasets: [
          {
            data: values,
            backgroundColor: colors.map((c) => c + "55"),
            borderColor: colors,
            borderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            grid: { color: "rgba(108,99,255,0.08)" },
            ticks: {
              color: "#6a6a8a",
              font: { size: 9 },
              backdropColor: "transparent",
              callback: (v) => `${v}%`,
            },
            pointLabels: {
              color: "#8888aa",
              font: { family: "DM Sans", size: 11 },
            },
          },
        },
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              color: "#8888aa",
              font: { family: "DM Sans", size: 11 },
              padding: 12,
              usePointStyle: true,
            },
          },
          tooltip: {
            backgroundColor: "#12121c",
            borderColor: "rgba(108,99,255,0.3)",
            borderWidth: 1,
            titleColor: "#e8e8f0",
            bodyColor: "#8888aa",
            padding: 10,
            callbacks: {
              label: (ctx) => ` ${ctx.raw.toFixed(1)}%`,
            },
          },
        },
        animation: { duration: 800 },
      },
    });

    return () => {
      if (chartRef.current) chartRef.current.destroy();
    };
  }, [data]);

  return (
    <div className="w-full" style={{ height: "250px" }}>
      <canvas ref={canvasRef} />
    </div>
  );
}
