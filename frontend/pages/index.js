import { useState } from "react";
import { useRouter } from "next/router";
import Head from "next/head";

const SUGGESTIONS = ["Tesla", "#AI", "iPhone", "OpenAI", "Bitcoin", "Netflix", "SpaceX"];

const PLATFORM_ICONS = {
  YouTube: { color: "#ff6584", icon: "▶" },
  Mastodon: { color: "#818cf8", icon: "🐘" },
  NewsAPI: { color: "#43e8a4", icon: "📰" },
  "Hacker News": { color: "#fbbf24", icon: "Y" },
};

export default function Home() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    router.push(`/dashboard?q=${encodeURIComponent(query.trim())}`);
  };

  const handleSuggestion = (s) => {
    setQuery(s);
  };

  return (
    <>
      <Head>
        <title>VibeScope — Social Sentiment Intelligence</title>
        <meta name="description" content="Real-time sentiment analysis across social platforms" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="relative min-h-screen bg-void overflow-hidden flex flex-col items-center justify-center px-4">
        {/* Background grid */}
        <div
          className="absolute inset-0 opacity-100"
          style={{
            backgroundImage:
              "linear-gradient(rgba(108,99,255,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(108,99,255,0.04) 1px, transparent 1px)",
            backgroundSize: "48px 48px",
          }}
        />

        {/* Radial glow */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            background:
              "radial-gradient(ellipse 70% 50% at 50% 0%, rgba(108,99,255,0.12), transparent 70%)",
          }}
        />

        {/* Floating orbs */}
        <div
          className="absolute w-72 h-72 rounded-full pointer-events-none"
          style={{
            background: "radial-gradient(circle, rgba(108,99,255,0.08) 0%, transparent 70%)",
            top: "10%",
            left: "5%",
            animation: "float 8s ease-in-out infinite",
          }}
        />
        <div
          className="absolute w-48 h-48 rounded-full pointer-events-none"
          style={{
            background: "radial-gradient(circle, rgba(255,101,132,0.06) 0%, transparent 70%)",
            bottom: "15%",
            right: "8%",
            animation: "float 10s ease-in-out infinite reverse",
          }}
        />

        {/* Content */}
        <div className="relative z-10 w-full max-w-2xl flex flex-col items-center gap-8">
          {/* Badge */}
          <div
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border text-xs font-mono tracking-wider"
            style={{
              borderColor: "rgba(108,99,255,0.3)",
              color: "#6c63ff",
              background: "rgba(108,99,255,0.06)",
            }}
          >
            <span className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse-slow" style={{ background: "#43e8a4" }} />
            LIVE SENTIMENT INTELLIGENCE
          </div>

          {/* Headline */}
          <div className="text-center">
            <h1
              className="text-6xl md:text-7xl font-display font-extrabold leading-none mb-4"
              style={{ letterSpacing: "-2px" }}
            >
              <span className="gradient-text">Vibe</span>
              <span className="text-white">Scope</span>
            </h1>
            <p className="text-lg text-muted font-body max-w-md mx-auto leading-relaxed" style={{ color: "#6a6a8a" }}>
              Decode public sentiment across YouTube, Mastodon, News & Hacker News — powered by transformer models
            </p>
          </div>

          {/* Search form */}
          <form onSubmit={handleSubmit} className="w-full">
            <div
              className="relative group rounded-2xl p-px"
              style={{
                background: "linear-gradient(135deg, rgba(108,99,255,0.4), rgba(255,101,132,0.2), rgba(67,232,164,0.2))",
              }}
            >
              <div className="flex items-center bg-panel rounded-2xl overflow-hidden" style={{ background: "#0f0f1a" }}>
                <span className="pl-5 text-xl" style={{ color: "#6c63ff" }}>⌕</span>
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Tesla, #AI, iPhone, Microsoft…"
                  className="flex-1 bg-transparent px-4 py-5 text-lg text-white outline-none font-body placeholder:text-muted"
                  style={{ caretColor: "#6c63ff" }}
                  autoFocus
                />
                <button
                  type="submit"
                  disabled={loading || !query.trim()}
                  className="m-2 px-6 py-3 rounded-xl font-display font-semibold text-sm transition-all duration-200 disabled:opacity-40"
                  style={{
                    background: "linear-gradient(135deg, #6c63ff, #8b84ff)",
                    color: "white",
                    boxShadow: "0 4px 20px rgba(108,99,255,0.35)",
                  }}
                >
                  {loading ? (
                    <span className="flex items-center gap-2">
                      <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin inline-block" />
                      Analyzing
                    </span>
                  ) : (
                    "Analyze →"
                  )}
                </button>
              </div>
            </div>
          </form>

          {/* Suggestions */}
          <div className="flex flex-wrap gap-2 justify-center">
            <span className="text-xs font-mono" style={{ color: "#4a4a6a" }}>Try:</span>
            {SUGGESTIONS.map((s) => (
              <button
                key={s}
                onClick={() => handleSuggestion(s)}
                className="px-3 py-1 rounded-lg text-sm border transition-all duration-150 hover:border-accent/50"
                style={{
                  borderColor: "rgba(108,99,255,0.2)",
                  color: "#8888aa",
                  background: "rgba(108,99,255,0.04)",
                }}
              >
                {s}
              </button>
            ))}
          </div>

          {/* Platform pills */}
          <div className="flex flex-wrap gap-3 justify-center mt-2">
            {Object.entries(PLATFORM_ICONS).map(([name, { color, icon }]) => (
              <div
                key={name}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-full border text-xs font-mono"
                style={{
                  borderColor: `${color}30`,
                  color,
                  background: `${color}08`,
                }}
              >
                <span>{icon}</span>
                {name}
              </div>
            ))}
          </div>
        </div>

        {/* Bottom fade */}
        <div
          className="absolute bottom-0 left-0 right-0 h-24 pointer-events-none"
          style={{
            background: "linear-gradient(transparent, rgba(5,5,8,0.8))",
          }}
        />
      </main>

      <style jsx global>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-16px); }
        }
      `}</style>
    </>
  );
}
