/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ["'Syne'", "sans-serif"],
        body: ["'DM Sans'", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      colors: {
        void: "#050508",
        surface: "#0d0d14",
        panel: "#12121c",
        border: "#1e1e2e",
        accent: "#6c63ff",
        "accent-2": "#ff6584",
        "accent-3": "#43e8a4",
        muted: "#4a4a6a",
        faint: "#2a2a3e",
        positive: "#43e8a4",
        negative: "#ff6584",
        neutral: "#6c63ff",
      },
      animation: {
        "pulse-slow": "pulse 3s ease-in-out infinite",
        "spin-slow": "spin 8s linear infinite",
        float: "float 6s ease-in-out infinite",
        "fade-up": "fadeUp 0.6s ease forwards",
        "glow-pulse": "glowPulse 2s ease-in-out infinite",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-12px)" },
        },
        fadeUp: {
          from: { opacity: "0", transform: "translateY(24px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        glowPulse: {
          "0%, 100%": { boxShadow: "0 0 20px rgba(108,99,255,0.3)" },
          "50%": { boxShadow: "0 0 40px rgba(108,99,255,0.7)" },
        },
      },
      backgroundImage: {
        "grid-pattern":
          "linear-gradient(rgba(108,99,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(108,99,255,0.03) 1px, transparent 1px)",
        "glow-radial":
          "radial-gradient(ellipse 80% 50% at 50% -20%, rgba(108,99,255,0.15), transparent)",
      },
      backgroundSize: {
        "grid-sm": "40px 40px",
      },
    },
  },
  plugins: [],
};
