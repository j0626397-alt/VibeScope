export default function TrendingKeywords({ keywords }) {
  if (!keywords?.length) {
    return (
      <div className="text-muted text-sm font-mono text-center py-8">
        No keywords found
      </div>
    );
  }

  const maxRank = keywords.length;

  return (
    <div className="flex flex-col gap-2 w-full">
      {keywords.map((kw, i) => {
        const barWidth = ((maxRank - i) / maxRank) * 100;
        const hue = Math.round((i / maxRank) * 120 + 200); // blue → green range
        const colors = [
          "#6c63ff", "#818cf8", "#a78bfa",
          "#43e8a4", "#34d399", "#6ee7b7",
          "#fbbf24", "#f59e0b", "#fcd34d",
          "#ff6584",
        ];
        const color = colors[i] || "#6c63ff";

        return (
          <div key={kw} className="flex items-center gap-3 group">
            {/* Rank */}
            <span
              className="w-6 text-right text-xs font-mono shrink-0"
              style={{ color: "#4a4a6a" }}
            >
              {String(i + 1).padStart(2, "0")}
            </span>

            {/* Bar + label */}
            <div className="flex-1 relative">
              <div
                className="rounded-sm h-7 flex items-center px-3 transition-all duration-500"
                style={{
                  width: `${barWidth}%`,
                  minWidth: "60px",
                  background: `${color}18`,
                  border: `1px solid ${color}30`,
                }}
              >
                <span
                  className="text-sm font-display font-semibold truncate"
                  style={{ color }}
                >
                  {kw}
                </span>
              </div>
            </div>

            {/* Trending indicator */}
            {i < 3 && (
              <span className="text-xs" style={{ color: "#43e8a4" }}>
                ↑
              </span>
            )}
          </div>
        );
      })}
    </div>
  );
}
