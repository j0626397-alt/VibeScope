"""
POST /api/analyze
Orchestrates: data fetch -> clean -> sentiment (RoBERTa) -> emotion (DistilRoBERTa) -> keywords -> summary
"""

import sys
import os
import asyncio
from datetime import datetime, timedelta

# Add ml_service to path
# ML_PATH = os.path.join(os.path.dirname(__file__), "../../ml_service")
# sys.path.insert(0, ML_PATH)

from fastapi import APIRouter, HTTPException
from backend.database.models import AnalyzeRequest, AnalyzeResponse
from backend.database.mongodb import get_db
from backend.services.youtube_service import fetch_youtube_posts
from backend.services.mastodon_service import fetch_mastodon_posts
from backend.services.news_service import fetch_news_posts
from backend.services.hackernews_service import fetch_hackernews_posts

router = APIRouter()


def _filter_posts_for_language(posts: list) -> list:
    """
    Filter posts to keep only valid English posts.
    Runs in executor to avoid blocking the event loop.
    """
    from ml_service.language_filter import filter_posts
    
    filtered_posts, filtered_count = filter_posts(posts)
    print(f"[Analyze] Language filter: {len(posts)} posts -> {len(filtered_posts)} posts (removed {filtered_count})")
    return filtered_posts


def _run_ml_pipeline(all_posts: list, query: str) -> dict:
    """
    Run the full ML pipeline synchronously (called via run_in_executor).
    Uses exact notebook implementations:
      - cardiffnlp/twitter-roberta-base-sentiment  (AutoTokenizer + AutoModel + softmax)
      - j-hartmann/emotion-english-distilroberta-base (pipeline)
      - NLTK keyword extraction
    """
    from ml_service.sentiment_model import analyze_sentiment, compute_sentiment_distribution
    from ml_service.emotion_detector import detect_emotion, compute_emotion_distribution
    from ml_service.keyword_extractor import extract_keywords_nltk, build_wordcloud_data
    from ml_service.summarizer import generate_summary

    # ── 1. Sentiment ────────────────────────────────────────────────
    print(f"[Pipeline] Running sentiment on {len(all_posts)} posts ...")
    for post in all_posts:
        result = analyze_sentiment(post["clean_text"])
        post["sentiment"] = result["label"]
        post["sentiment_score"] = result["score"]

    # ── 2. Emotion ──────────────────────────────────────────────────
    print("[Pipeline] Running emotion detection ...")
    for post in all_posts:
        post["emotion"] = detect_emotion(post["clean_text"])

    # ── 3. Distributions ────────────────────────────────────────────
    all_sentiments = [p["sentiment"] for p in all_posts]
    sentiment_distribution = compute_sentiment_distribution(all_sentiments)

    all_emotions = [p["emotion"] for p in all_posts]
    emotion_distribution = compute_emotion_distribution(all_emotions)

    # ── 4. Per-platform breakdown ────────────────────────────────────
    platform_sentiment = {}
    for platform in ["youtube", "mastodon", "news", "hackernews"]:
        pf_posts = [p for p in all_posts if p["platform"] == platform]
        pf_sentiments = [p["sentiment"] for p in pf_posts]
        platform_sentiment[platform] = compute_sentiment_distribution(pf_sentiments)

    # ── 5. Keywords + word cloud ─────────────────────────────────────
    texts = [p["clean_text"] for p in all_posts]
    trending_keywords = extract_keywords_nltk(texts, top_n=10)
    wordcloud_data = build_wordcloud_data(texts, top_n=60)

    # ── 6. Example posts (one per sentiment bucket) ──────────────────
    example_posts = {}
    for sentiment in ["positive", "neutral", "negative"]:
        matches = [p for p in all_posts if p["sentiment"] == sentiment]
        if matches:
            # pick the one with highest confidence score
            best = max(matches, key=lambda p: p.get("sentiment_score", 0))
            example_posts[sentiment] = best["text"][:400]

    # ── 7. Summary ───────────────────────────────────────────────────
    summary = generate_summary(query, all_posts, sentiment_distribution, emotion_distribution)

    return {
        "sentiment_distribution": sentiment_distribution,
        "platform_sentiment": platform_sentiment,
        "emotion_distribution": emotion_distribution,
        "trending_keywords": trending_keywords,
        "wordcloud_data": wordcloud_data,
        "example_posts": example_posts,
        "summary": summary,
    }


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    db = get_db()

    # Check MongoDB cache (5-min TTL)
    if db is not None:
        cached = await db.analysis_results.find_one({
            "query": query.lower(),
            "created_at": {"$gte": datetime.utcnow() - timedelta(minutes=5)},
        })
        if cached:
            cached.pop("_id", None)
            return AnalyzeResponse(**cached, cached=True)

    # ── Parallel data fetch ──────────────────────────────────────────
    youtube_posts, mastodon_posts, news_posts, hn_posts = await asyncio.gather(
        fetch_youtube_posts(query, max_posts=50),
        fetch_mastodon_posts(query, max_posts=50),
        fetch_news_posts(query, max_posts=50),
        fetch_hackernews_posts(query, max_posts=50),
    )

    all_posts = [*youtube_posts, *mastodon_posts, *news_posts, *hn_posts]

    if not all_posts:
        raise HTTPException(status_code=404, detail="No posts found for this query")

    print(f"[Analyze] Total posts collected: {len(all_posts)}")

    # ── Language filtering (off event loop) ──────────────────────────
    loop = asyncio.get_event_loop()
    all_posts = await loop.run_in_executor(None, _filter_posts_for_language, all_posts)

    if not all_posts:
        raise HTTPException(status_code=404, detail="No English posts found for this query")

    # ── ML pipeline (off event loop) ────────────────────────────────
    ml_results = await loop.run_in_executor(None, _run_ml_pipeline, all_posts, query)

    result = {
        "query": query.lower(),
        "total_posts": len(all_posts),
        "created_at": datetime.utcnow(),
        **ml_results,
    }

    # Store in MongoDB
    if db is not None:
        try:
            await db.analysis_results.insert_one(dict(result))
        except Exception as e:
            print(f"[MongoDB] Insert failed: {e}")

    result.pop("created_at", None)
    result.pop("_id", None)

    return AnalyzeResponse(**result)
