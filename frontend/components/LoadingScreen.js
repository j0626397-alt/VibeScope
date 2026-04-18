const STAGES = [
  { label: "Fetching YouTube", icon: "▶", color: "#ff6584" },
  { label: "Scraping Mastodon", icon: "🐘", color: "#818cf8" },
  { label: "Reading NewsAPI", icon: "📰", color: "#43e8a4" },
  { label: "Scanning Hacker News", icon: "Y", color: "#fbbf24" },
  { label: "Running RoBERTa sentiment model", icon: "🧠", color: "#6c63ff" },
  { label: "Detecting emotions", icon: "💡", color: "#a78bfa" },
  { label: "Extracting keywords", icon: "🔍", color: "#43e8a4" },
  { label: "Generating summary", icon: "✍️", color: "#ff6584" },
];

export default function LoadingScreen({ query }) {
  return (
    <div className="fixed inset-0 z-50 flex flex-col items-center justify-center" style={{ background: "#050508" }}>
      {/* Background grid */}
      <div
        className="absolute inset-0 opacity-100"
        style={{
          backgroundImage:
            "linear-gradient(rgba(108,99,255,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(108,99,255,0.04) 1px, transparent 1px)",
          backgroundSize: "48px 48px",
        }}
      />

      <div className="relative z-10 flex flex-col items-center gap-8 max-w-sm w-full px-6">
        {/* Spinner */}
        <div className="relative w-20 h-20">
          <div
            className="absolute inset-0 rounded-full border-2 border-transparent animate-spin"
            style={{
              borderTopColor: "#6c63ff",
              borderRightColor: "#ff6584",
              animationDuration: "1.2s",
            }}
          />
          <div
            className="absolute inset-2 rounded-full border border-transparent animate-spin"
            style={{
              borderTopColor: "#43e8a4",
              animationDuration: "2s",
              animationDirection: "reverse",
            }}
          />
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-2xl font-display font-bold gradient-text">VS</span>
          </div>
        </div>

        {/* Query */}
        <div className="text-center">
          <p className="text-sm font-mono mb-1" style={{ color: "#4a4a6a" }}>
            ANALYZING
          </p>
          <p className="text-2xl font-display font-bold text-white">
            "{query}"
          </p>
        </div>

        {/* Stage list */}
        <div className="w-full flex flex-col gap-2">
          {STAGES.map((stage, i) => (
            <div
              key={stage.label}
              className="flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm"
              style={{
                background: "rgba(18,18,28,0.8)",
                border: "1px solid rgba(108,99,255,0.1)",
                animation: `fadeIn 0.4s ease forwards`,
                animationDelay: `${i * 0.2}s`,
                opacity: 0,
              }}
            >
              <span>{stage.icon}</span>
              <span style={{ color: "#6a6a8a" }}>{stage.label}</span>
              <div className="ml-auto flex gap-1">
                {[0, 1, 2].map((dot) => (
                  <div
                    key={dot}
                    className="w-1 h-1 rounded-full"
                    style={{
                      background: stage.color,
                      animation: "bounce 1.4s ease-in-out infinite",
                      animationDelay: `${i * 0.1 + dot * 0.2}s`,
                    }}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateX(-8px); }
          to { opacity: 1; transform: translateX(0); }
        }
        @keyframes bounce {
          0%, 80%, 100% { transform: scaleY(0.4); opacity: 0.4; }
          40% { transform: scaleY(1); opacity: 1; }
        }
      `}</style>
    </div>
  );
}
