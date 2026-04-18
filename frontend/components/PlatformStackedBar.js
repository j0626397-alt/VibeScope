import { useEffect, useRef } from "react";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const PLATFORM_LABELS = {
  youtube: "YouTube",
  mastodon: "Mastodon",
  news: "News",
  hackernews: "Hacker News",
};

const PLATFORM_COLORS = {
  youtube: "#ff6584",
  mastodon: "#818cf8",
  news: "#43e8a4",
  hackernews: "#fbbf24",
};

const SENTIMENT_COLORS = {
  positive: "#43e8a4",
  neutral: "#6c63ff",
  negative: "#ff6584",
};

export default function PlatformStackedBar({ data }) {
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current || !data) return;

    if (chartRef.current) {
      chartRef.current.destroy();
    }

    const platforms = Object.keys(data);
    const platformLabels = platforms.map((p) => PLATFORM_LABELS[p] || p);

    const datasets = ["positive", "neutral", "negative"].map((sentiment) => ({
      label: sentiment.charAt(0).toUpperCase() + sentiment.slice(1),
      data: platforms.map((p) => data[p]?.[sentiment] ?? 0),
      backgroundColor: SENTIMENT_COLORS[sentiment] + "bb",
      borderColor: SENTIMENT_COLORS[sentiment],
      borderWidth: 1,
      borderRadius: 4,
    }));

    chartRef.current = new Chart(canvasRef.current, {
      type: "bar",
      data: { labels: platformLabels, datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: "x",
        scales: {
          x: {
            stacked: true,
            grid: { color: "rgba(108,99,255,0.06)" },
            ticks: {
              color: "#6a6a8a",
              font: { family: "DM Sans", size: 11 },
            },
            border: { color: "rgba(108,99,255,0.1)" },
          },
          y: {
            stacked: true,
            min: 0,
            max: 100,
            grid: { color: "rgba(108,99,255,0.06)" },
            ticks: {
              color: "#6a6a8a",
              font: { family: "DM Sans", size: 11 },
              callback: (v) => `${v}%`,
            },
            border: { color: "rgba(108,99,255,0.1)" },
          },
        },
        plugins: {
          legend: {
            position: "top",
            align: "end",
            labels: {
              color: "#8888aa",
              font: { family: "DM Sans", size: 11 },
              padding: 12,
              usePointStyle: true,
              pointStyleWidth: 7,
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
              label: (ctx) => ` ${ctx.dataset.label}: ${ctx.raw.toFixed(1)}%`,
            },
          },
        },
        animation: { duration: 800, easing: "easeInOutQuart" },
      },
    });

    return () => {
      if (chartRef.current) chartRef.current.destroy();
    };
  }, [data]);

  return (
    <div className="w-full" style={{ height: "240px" }}>
      <canvas ref={canvasRef} />
    </div>
  );
}
