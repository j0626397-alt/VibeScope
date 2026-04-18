# VibeScope 🔍

**Real-time social media sentiment analysis platform** — powered by RoBERTa transformers, FastAPI, Next.js, and MongoDB.

Analyze public opinion about any keyword, hashtag, brand, or topic across **YouTube**, **Mastodon**, **NewsAPI**, and **Hacker News** — with AI-generated summaries, emotion detection, keyword extraction, and interactive dashboards.

---

## Architecture

```
vibescope/
├── frontend/          # Next.js 14 + Tailwind + Chart.js dashboard
├── backend/           # FastAPI async REST API
│   ├── routes/        # /analyze, /posts, /history
│   ├── services/      # Per-platform data fetchers
│   ├── pipeline/      # Text cleaning & preprocessing
│   └── database/      # MongoDB motor models
├── ml-service/        # HuggingFace sentiment, emotion, keywords, summarizer
└── database/          # Seed data script
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14, Tailwind CSS, Chart.js, React Query |
| Backend | FastAPI, Python 3.11+, async/await |
| ML/NLP | HuggingFace Transformers (`cardiffnlp/twitter-roberta-base-sentiment`) |
| Emotion | Lexicon-based rule engine |
| Summarizer | `facebook/bart-large-cnn` (with rule-based fallback) |
| Database | MongoDB via Motor (async) |
| Data APIs | YouTube Data v3, Mastodon, NewsAPI, Hacker News Firebase |

---

## Quickstart

### 1. Clone & Setup

```bash
git clone https://github.com/yourname/vibescope
cd vibescope
cp .env.example .env
# Fill in your API keys in .env
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r ../requirements.txt

# Start server
uvicorn main:app --reload --port 8000
```

API available at: `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard at: `http://localhost:3000`

### 4. MongoDB (optional — graceful fallback if unavailable)

```bash
# macOS
brew install mongodb-community && brew services start mongodb-community

# Ubuntu
sudo systemctl start mongod

# Docker
docker run -d -p 27017:27017 mongo:7
```

Seed with sample data:
```bash
cd vibescope
python database/seed_data.py
```

---

## API Keys Setup

| Service | Where to get it | Required? |
|---|---|---|
| `YOUTUBE_API_KEY` | [Google Cloud Console](https://console.developers.google.com/) → YouTube Data API v3 | Optional (mock data fallback) |
| `MASTODON_TOKEN` | [mastodon.social](https://mastodon.social/settings/applications) → New Application | Optional (public API works without token) |
| `NEWS_API_KEY` | [newsapi.org/register](https://newsapi.org/register) | Optional (mock data fallback) |
| `MONGODB_URI` | Local MongoDB or [MongoDB Atlas](https://cloud.mongodb.com/) | Optional (results won't be cached) |

> **No API keys required to run!** All services have mock data fallbacks so you can test immediately.

---

## API Reference

### `POST /api/analyze`

Analyze sentiment for a query across all platforms.

**Request:**
```json
{ "query": "Tesla" }
```

**Response:**
```json
{
  "query": "tesla",
  "sentiment_distribution": {
    "positive": 54.2,
    "neutral": 28.1,
    "negative": 17.7
  },
  "platform_sentiment": {
    "youtube": { "positive": 62.0, "neutral": 22.0, "negative": 16.0 },
    "mastodon": { "positive": 41.0, "neutral": 35.0, "negative": 24.0 },
    "news":     { "positive": 55.0, "neutral": 30.0, "negative": 15.0 },
    "hackernews": { "positive": 49.0, "neutral": 28.0, "negative": 23.0 }
  },
  "emotion_distribution": {
    "happy": 32.5, "excitement": 28.1, "neutral": 22.4,
    "anger": 10.3, "sadness": 6.7
  },
  "trending_keywords": ["model", "launch", "price", "battery", "autopilot"],
  "wordcloud_data": { "model": 95, "launch": 82, "tesla": 75 },
  "example_posts": {
    "positive": "Tesla's new Autopilot update is mind-blowing!",
    "neutral": "Tesla announces Q4 earnings next week.",
    "negative": "Disappointed with the recent service quality at Tesla."
  },
  "summary": "Public sentiment around Tesla is largely positive...",
  "total_posts": 187,
  "cached": false
}
```

### `GET /api/posts?query=Tesla&platform=youtube&sentiment=positive`

Retrieve stored individual posts with optional filters.

### `GET /api/history`

Get recent analysis queries.

---

## ML Pipeline

```
User query
    │
    ▼
Parallel data fetch (asyncio.gather)
├── YouTube Data API → video search → comment threads
├── Mastodon API → hashtag timeline
├── NewsAPI → article titles + descriptions
└── HackerNews → top stories filtered by keyword
    │
    ▼
Text cleaning pipeline
├── HTML tag removal
├── URL stripping
├── Emoji removal
├── Special char normalization
└── Truncation to 512 tokens
    │
    ▼
ML inference (thread pool)
├── Sentiment: cardiffnlp/twitter-roberta-base-sentiment
│   LABEL_0 → negative | LABEL_1 → neutral | LABEL_2 → positive
├── Emotion: lexicon-based (happy/anger/sadness/excitement/neutral)
├── Keywords: frequency analysis, top-10
└── Summary: facebook/bart-large-cnn (rule-based fallback)
    │
    ▼
Store in MongoDB (5-min TTL cache)
    │
    ▼
JSON response → Next.js Dashboard
```

---

## Dashboard Features

| Panel | Description |
|---|---|
| 🥧 Sentiment Pie | Positive/Neutral/Negative % with dominant label |
| 📊 Platform Breakdown | Stacked bar: sentiment per platform |
| 🌀 Emotion Distribution | Polar area chart: happy/anger/sadness/excitement |
| ☁️ Word Cloud | Frequency-weighted, color-coded term cloud |
| 📈 Trending Keywords | Ranked bar list of top 10 terms |
| 💬 Example Posts | One real post per sentiment bucket |
| ✦ AI Summary | Narrative summary of overall public opinion |

---

## Environment Variables

```bash
# .env
MONGODB_URI=mongodb://localhost:27017
YOUTUBE_API_KEY=...
MASTODON_TOKEN=...
NEWS_API_KEY=...
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

---

## Development Notes

- **Mock fallbacks**: All 4 platform services return realistic mock data if API keys are missing — ideal for local development.
- **Caching**: Results are cached in MongoDB for 5 minutes to avoid redundant ML inference.
- **Model loading**: RoBERTa is loaded once and cached via `@lru_cache` — first request is slow (~10–30s), subsequent ones are fast.
- **Async**: Backend uses `asyncio.gather` for parallel data fetching and `run_in_executor` to keep ML inference off the event loop.

---

## License

MIT
