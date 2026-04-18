"""
LLM Summary generator.
Uses facebook/bart-large-cnn via HuggingFace pipeline (as specified in prompt),
with a robust rule-based narrative fallback.
"""

import os
from typing import List, Dict

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def generate_summary(
    query: str,
    posts: List[dict],
    sentiment_dist: Dict[str, float],
    emotion_dist: Dict[str, float],
) -> str:
    """Generate narrative summary — BART first, rule-based fallback."""
    try:
        return _bart_summarize(query, posts, sentiment_dist)
    except Exception as e:
        print(f"[Summarizer] BART failed ({e}), using rule-based fallback")
        return _rule_based_summary(query, sentiment_dist, emotion_dist, len(posts))


def _bart_summarize(query: str, posts: List[dict], sentiment_dist: Dict) -> str:
    from transformers import pipeline

    pos = sentiment_dist.get("positive", 0)
    neg = sentiment_dist.get("negative", 0)
    neu = sentiment_dist.get("neutral", 0)

    # Build representative context from top posts
    sample = [p["clean_text"] for p in posts[:40] if p.get("clean_text")]
    combined = " ".join(sample)[:1500]

    prompt = (
        f"Summarize public sentiment about '{query}'. "
        f"Sentiment: {pos:.0f}% positive, {neg:.0f}% negative, {neu:.0f}% neutral. "
        f"Sample posts: {combined}"
    )

    summarizer = pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        device=-1,
    )
    result = summarizer(
        prompt[:1024],
        max_length=120,
        min_length=40,
        do_sample=False,
    )
    return result[0]["summary_text"]


def _rule_based_summary(
    query: str,
    sentiment_dist: Dict[str, float],
    emotion_dist: Dict[str, float],
    total: int,
) -> str:
    pos = sentiment_dist.get("positive", 0)
    neg = sentiment_dist.get("negative", 0)
    neu = sentiment_dist.get("neutral", 0)

    dominant_emotion = max(emotion_dist, key=emotion_dist.get) if emotion_dist else "neutral"
    emotion_pct = emotion_dist.get(dominant_emotion, 0)

    if pos >= 55:
        tone = f"largely positive ({pos:.0f}% of posts expressing support and enthusiasm)"
    elif neg >= 55:
        tone = f"largely negative ({neg:.0f}% of posts expressing concern or criticism)"
    elif pos > neg:
        tone = f"mixed but leaning positive ({pos:.0f}% positive vs {neg:.0f}% negative)"
    elif neg > pos:
        tone = f"mixed but leaning negative ({neg:.0f}% negative vs {pos:.0f}% positive)"
    else:
        tone = f"predominantly neutral ({neu:.0f}% of posts taking a balanced stance)"

    emotion_phrases = {
        "happy":      "enthusiasm and satisfaction",
        "excitement": "excitement and anticipation",
        "anger":      "frustration and dissatisfaction",
        "sadness":    "disappointment and concern",
        "neutral":    "measured and objective discussion",
    }
    emotion_phrase = emotion_phrases.get(dominant_emotion, "varied emotional responses")

    outcome = "broad appeal" if pos > 50 else ("growing concern" if neg > 40 else "ongoing debate")

    return (
        f"Public sentiment around '{query}' is {tone}. "
        f"Across {total} posts analyzed from YouTube, Mastodon, News, and Hacker News, "
        f"the dominant emotional tone reflects {emotion_phrase} ({emotion_pct:.0f}%). "
        f"The conversation spans multiple platforms, suggesting {outcome} around {query}."
    )
