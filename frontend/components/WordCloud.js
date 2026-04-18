import { useMemo } from "react";

const ACCENT_COLORS = [
  "#6c63ff", "#ff6584", "#43e8a4", "#fbbf24",
  "#818cf8", "#f472b6", "#34d399", "#a78bfa",
];

export default function WordCloud({ data }) {
  const words = useMemo(() => {
    if (!data) return [];

    const entries = Object.entries(data).sort(([, a], [, b]) => b - a);
    if (!entries.length) return [];

    const maxFreq = entries[0][1];

    return entries.slice(0, 40).map(([word, freq], i) => {
      const ratio = freq / maxFreq;
      const size = Math.max(11, Math.round(12 + ratio * 28));
      const color = ACCENT_COLORS[i % ACCENT_COLORS.length];
      const opacity = 0.5 + ratio * 0.5;
      return { word, freq, size, color, opacity };
    });
  }, [data]);

  if (!words.length) {
    return (
      <div className="flex items-center justify-center h-40 text-muted text-sm font-mono">
        No keyword data
      </div>
    );
  }

  return (
    <div className="w-full flex flex-wrap gap-2 justify-center items-center py-4 px-2">
      {words.map(({ word, size, color, opacity }) => (
        <span
          key={word}
          className="cursor-default select-none transition-all duration-200 hover:opacity-100 hover:scale-110 inline-block"
          style={{
            fontSize: `${size}px`,
            color,
            opacity,
            fontFamily: "'Syne', sans-serif",
            fontWeight: size > 28 ? 700 : size > 18 ? 600 : 500,
            lineHeight: 1.3,
            letterSpacing: "-0.02em",
            textShadow: `0 0 20px ${color}44`,
          }}
        >
          {word}
        </span>
      ))}
    </div>
  );
}
