import { useEffect, useRef } from "react";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const COLORS = {
  positive: "#43e8a4",
  neutral: "#6c63ff",
  negative: "#ff6584",
};

export default function SentimentPie({ data }) {
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current || !data) return;

    if (chartRef.current) {
      chartRef.current.destroy();
    }

    const labels = Object.keys(data);
    const values = Object.values(data);
    const colors = labels.map((l) => COLORS[l] || "#6c63ff");

    chartRef.current = new Chart(canvasRef.current, {
      type: "doughnut",
      data: {
        labels: labels.map((l) => l.charAt(0).toUpperCase() + l.slice(1)),
        datasets: [
          {
            data: values,
            backgroundColor: colors.map((c) => c + "cc"),
            borderColor: colors,
            borderWidth: 2,
            hoverBackgroundColor: colors,
            hoverBorderWidth: 3,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "68%",
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              color: "#8888aa",
              font: { family: "DM Sans", size: 12 },
              padding: 16,
              usePointStyle: true,
              pointStyleWidth: 8,
            },
          },
          tooltip: {
            backgroundColor: "#12121c",
            borderColor: "rgba(108,99,255,0.3)",
            borderWidth: 1,
            titleColor: "#e8e8f0",
            bodyColor: "#8888aa",
            padding: 12,
            callbacks: {
              label: (ctx) => ` ${ctx.label}: ${ctx.raw.toFixed(1)}%`,
            },
          },
        },
        animation: {
          duration: 800,
          easing: "easeInOutQuart",
        },
      },
    });

    return () => {
      if (chartRef.current) chartRef.current.destroy();
    };
  }, [data]);

  // Dominant sentiment
  const dominant = data
    ? Object.entries(data).sort(([, a], [, b]) => b - a)[0]
    : null;

  return (
    <div className="flex flex-col items-center gap-4">
      <div className="relative w-full" style={{ height: "220px" }}>
        <canvas ref={canvasRef} />
        {dominant && (
          <div
            className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none"
            style={{ top: "-10px" }}
          >
            <span
              className="text-3xl font-display font-bold"
              style={{ color: COLORS[dominant[0]] }}
            >
              {dominant[1].toFixed(0)}%
            </span>
            <span className="text-xs font-mono capitalize" style={{ color: "#6a6a8a" }}>
              {dominant[0]}
            </span>
          </div>
        )}
      </div>

      {/* Stat pills */}
      {data && (
        <div className="flex gap-3 flex-wrap justify-center">
          {Object.entries(data).map(([sentiment, pct]) => (
            <div
              key={sentiment}
              className="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono"
              style={{
                background: `${COLORS[sentiment]}14`,
                color: COLORS[sentiment],
                border: `1px solid ${COLORS[sentiment]}30`,
              }}
            >
              <span
                className="w-1.5 h-1.5 rounded-full"
                style={{ background: COLORS[sentiment] }}
              />
              {sentiment}: {pct.toFixed(1)}%
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
