import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import Head from "next/head";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { analyzeQuery } from "../utils/api";
import SentimentPie from "../components/SentimentPie";
import PlatformStackedBar from "../components/PlatformStackedBar";
import EmotionChart from "../components/EmotionChart";
import WordCloud from "../components/WordCloud";
import TrendingKeywords from "../components/TrendingKeywords";
import LoadingScreen from "../components/LoadingScreen";

const SENTIMENT_COLORS = {
  positive: { bg: "rgba(67,232,164,0.08)", border: "rgba(67,232,164,0.25)", text: "#43e8a4" },
  neutral: { bg: "rgba(108,99,255,0.08)", border: "rgba(108,99,255,0.25)", text: "#6c63ff" },
  negative: { bg: "rgba(255,101,132,0.08)", border: "rgba(255,101,132,0.25)", text: "#ff6584" },
};

const SENTIMENT_EMOJIS = { positive: "✨", neutral: "💭", negative: "⚠️" };

function Panel({ title, subtitle, children, className = "", style = {} }) {
  return (
    <div
      className={`rounded-2xl p-5 card-hover ${className}`}
      style={{
        background: "rgba(13,13,20,0.8)",
        border: "1px solid rgba(108,99,255,0.12)",
        ...style,
      }}
    >
      {(title || subtitle) && (
        <div className="mb-4">
          {title && (
            <h3 className="text-sm font-mono uppercase tracking-widest mb-0.5" style={{ color: "#4a4a6a" }}>
              {title}
            </h3>
          )}
          {subtitle && (
            <p className="text-xs" style={{ color: "#3a3a5a" }}>
              {subtitle}
            </p>
          )}
        </div>
      )}
      {children}
    </div>
  );
}

function StatCard({ label, value, color, icon }) {
  return (
    <div
      className="rounded-xl px-4 py-3 flex items-center gap-3"
      style={{ background: `${color}0d`, border: `1px solid ${color}28` }}
    >
      <span className="text-2xl">{icon}</span>
      <div>
        <div className="text-xl font-display font-bold" style={{ color }}>
          {value}
        </div>
        <div className="text-xs font-mono" style={{ color: "#4a4a6a" }}>
          {label}
        </div>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const router = useRouter();
  const { q: query } = router.query;
  const [searchInput, setSearchInput] = useState("");

  useEffect(() => {
    if (query) setSearchInput(query);
  }, [query]);

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["analyze", query],
    queryFn: () => analyzeQuery(query),
    enabled: !!query,
    staleTime: 5 * 60 * 1000,
  });

  const handleSearch = (e) => {
    e.preventDefault();
    if (!searchInput.trim()) return;
    router.push(`/dashboard?q=${encodeURIComponent(searchInput.trim())}`);
  };

  if (isLoading) return <LoadingScreen query={query} />;

  return (
    <>
      <Head>
        <title>{query ? `${query} — VibeScope` : "VibeScope Dashboard"}</title>
      </Head>

      <div
        className="min-h-screen"
        style={{
          background: "#050508",
          backgroundImage:
            "linear-gradient(rgba(108,99,255,0.025) 1px, transparent 1px), linear-gradient(90deg, rgba(108,99,255,0.025) 1px, transparent 1px)",
          backgroundSize: "48px 48px",
        }}
      >
        {/* Header */}
        <header
          className="sticky top-0 z-40 flex items-center gap-4 px-6 py-4"
          style={{
            background: "rgba(5,5,8,0.85)",
            backdropFilter: "blur(12px)",
            borderBottom: "1px solid rgba(108,99,255,0.1)",
          }}
        >
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 shrink-0">
            <div
              className="w-8 h-8 rounded-lg flex items-center justify-center text-sm font-display font-bold"
              style={{ background: "linear-gradient(135deg, #6c63ff, #8b84ff)" }}
            >
              VS
            </div>
            <span className="font-display font-bold text-white text-sm hidden sm:block">VibeScope</span>
          </Link>

          {/* Search bar */}
          <form onSubmit={handleSearch} className="flex-1 max-w-lg">
            <div
              className="flex items-center rounded-xl overflow-hidden"
              style={{ background: "rgba(18,18,28,0.9)", border: "1px solid rgba(108,99,255,0.18)" }}
            >
              <span className="pl-4 text-base" style={{ color: "#6c63ff" }}>⌕</span>
              <input
                type="text"
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                placeholder="New query…"
                className="flex-1 bg-transparent px-3 py-2.5 text-sm text-white outline-none"
                style={{ caretColor: "#6c63ff" }}
              />
              <button
                type="submit"
                className="px-4 py-2.5 text-xs font-mono transition-colors"
                style={{ color: "#6c63ff", borderLeft: "1px solid rgba(108,99,255,0.15)" }}
              >
                RUN →
              </button>
            </div>
          </form>

          {/* Meta */}
          {data && (
            <div
              className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-mono"
              style={{ background: "rgba(67,232,164,0.06)", color: "#43e8a4", border: "1px solid rgba(67,232,164,0.18)" }}
            >
              <span className="w-1.5 h-1.5 rounded-full bg-current animate-pulse" />
              {data.total_posts} posts · {data.cached ? "cached" : "live"}
            </div>
          )}
        </header>

        {/* Error */}
        {error && (
          <div className="max-w-2xl mx-auto mt-12 px-6">
            <div
              className="rounded-2xl p-6 text-center"
              style={{ background: "rgba(255,101,132,0.06)", border: "1px solid rgba(255,101,132,0.2)" }}
            >
              <p className="text-2xl mb-2">⚠️</p>
              <p className="font-display font-semibold text-white mb-1">Analysis Failed</p>
              <p className="text-sm" style={{ color: "#6a6a8a" }}>
                {error.response?.data?.detail || "Could not connect to backend. Make sure the API server is running."}
              </p>
              <button
                onClick={() => refetch()}
                className="mt-4 px-5 py-2 rounded-lg text-sm font-mono"
                style={{ background: "rgba(255,101,132,0.12)", color: "#ff6584", border: "1px solid rgba(255,101,132,0.25)" }}
              >
                Retry
              </button>
            </div>
          </div>
        )}

        {/* Empty state */}
        {!query && !isLoading && (
          <div className="flex flex-col items-center justify-center h-96 gap-4">
            <p className="text-4xl">🔍</p>
            <p className="font-display font-semibold text-white">No query yet</p>
            <Link href="/" className="text-sm font-mono" style={{ color: "#6c63ff" }}>
              ← Go to search
            </Link>
          </div>
        )}

        {/* Dashboard content */}
        {data && (
          <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8 flex flex-col gap-6">
            {/* Query heading */}
            <div className="flex items-start justify-between gap-4 flex-wrap">
              <div>
                <p className="text-xs font-mono mb-1" style={{ color: "#4a4a6a" }}>
                  SENTIMENT REPORT FOR
                </p>
                <h1 className="text-3xl sm:text-4xl font-display font-extrabold text-white" style={{ letterSpacing: "-1px" }}>
                  {data.query}
                </h1>
              </div>
              <div className="flex gap-3 flex-wrap">
                <StatCard label="Total Posts" value={data.total_posts} color="#6c63ff" icon="📊" />
                <StatCard
                  label="Dominant Mood"
                  value={Object.entries(data.sentiment_distribution).sort(([,a],[,b])=>b-a)[0]?.[0] || "—"}
                  color="#43e8a4"
                  icon="🎯"
                />
              </div>
            </div>

            {/* LLM Summary */}
            <div
              className="rounded-2xl p-6"
              style={{
                background: "linear-gradient(135deg, rgba(108,99,255,0.08), rgba(67,232,164,0.04))",
                border: "1px solid rgba(108,99,255,0.2)",
              }}
            >
              <div className="flex items-center gap-2 mb-3">
                <span className="text-sm font-mono" style={{ color: "#6c63ff" }}>✦ AI SUMMARY</span>
              </div>
              <p className="text-base leading-relaxed" style={{ color: "#c8c8e0", fontStyle: "italic" }}>
                "{data.summary}"
              </p>
            </div>

            {/* Row 1: Pie + Platform */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Panel title="Sentiment Distribution" subtitle="Positive · Neutral · Negative">
                <SentimentPie data={data.sentiment_distribution} />
              </Panel>
              <Panel title="Platform Breakdown" subtitle="Stacked sentiment by source">
                <PlatformStackedBar data={data.platform_sentiment} />
              </Panel>
            </div>

            {/* Row 2: Emotions + Keywords */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Panel title="Emotion Distribution" subtitle="Detected emotional tones">
                <EmotionChart data={data.emotion_distribution} />
              </Panel>
              <Panel title="Trending Keywords" subtitle="Top 10 most frequent terms">
                <TrendingKeywords keywords={data.trending_keywords} />
              </Panel>
            </div>

            {/* Row 3: Word Cloud full width */}
            <Panel title="Word Cloud" subtitle="Frequency-weighted term visualization">
              <WordCloud data={data.wordcloud_data} />
            </Panel>

            {/* Row 4: Example posts */}
            <div>
              <p className="text-xs font-mono mb-4 uppercase tracking-widest" style={{ color: "#4a4a6a" }}>
                Example Posts by Sentiment
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {["positive", "neutral", "negative"].map((sentiment) => {
                  const text = data.example_posts?.[sentiment];
                  const cfg = SENTIMENT_COLORS[sentiment];
                  return (
                    <div
                      key={sentiment}
                      className="rounded-2xl p-5 flex flex-col gap-3"
                      style={{ background: cfg.bg, border: `1px solid ${cfg.border}` }}
                    >
                      <div className="flex items-center gap-2">
                        <span className="text-lg">{SENTIMENT_EMOJIS[sentiment]}</span>
                        <span
                          className="text-xs font-mono uppercase tracking-wider"
                          style={{ color: cfg.text }}
                        >
                          {sentiment}
                        </span>
                      </div>
                      {text ? (
                        <p className="text-sm leading-relaxed" style={{ color: "#9898b8" }}>
                          "{text}"
                        </p>
                      ) : (
                        <p className="text-sm italic" style={{ color: "#4a4a6a" }}>
                          No {sentiment} posts found
                        </p>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Footer */}
            <div
              className="text-center py-4 text-xs font-mono"
              style={{ color: "#2a2a4a", borderTop: "1px solid rgba(108,99,255,0.08)" }}
            >
              VibeScope · Powered by cardiffnlp/twitter-roberta-base-sentiment · {new Date().getFullYear()}
            </div>
          </main>
        )}
      </div>
    </>
  );
}
