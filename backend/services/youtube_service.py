"""
YouTube Data API v3 — fetch comments from videos matching a search query.
Falls back to realistic mock data when no API key is set.
"""

import os
import asyncio
from typing import List, Dict
from backend.pipeline.data_cleaning import clean_text, is_valid_text

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")


def _search_and_fetch(query: str, max_posts: int) -> List[Dict]:
    """Synchronous YouTube fetch — runs in thread pool."""
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    # Search for relevant videos
    search_resp = youtube.search().list(
        part="id",
        q=query,
        type="video",
        maxResults=5,
        order="relevance",
        relevanceLanguage="en",
    ).execute()

    video_ids = [item["id"]["videoId"] for item in search_resp.get("items", [])]
    posts = []

    per_video = max(10, max_posts // max(len(video_ids), 1))

    for vid_id in video_ids:
        if len(posts) >= max_posts:
            break
        try:
            resp = youtube.commentThreads().list(
                part="snippet",
                videoId=vid_id,
                maxResults=min(100, per_video),
                textFormat="plainText",
            ).execute()

            for item in resp.get("items", []):
                raw = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                cleaned = clean_text(raw)
                if is_valid_text(cleaned):
                    posts.append({"text": raw, "clean_text": cleaned, "platform": "youtube"})

        except HttpError:
            continue

    return posts[:max_posts]


async def fetch_youtube_posts(query: str, max_posts: int = 50) -> List[Dict]:
    if not YOUTUBE_API_KEY:
        return _mock_youtube_posts(query)

    loop = asyncio.get_event_loop()
    try:
        return await loop.run_in_executor(None, _search_and_fetch, query, max_posts)
    except Exception as e:
        print(f"[YouTube] API error: {e}, using mock data")
        return _mock_youtube_posts(query)


def _mock_youtube_posts(query: str) -> List[Dict]:
    """
    Realistic varied comments — deliberately covers positive, negative, neutral
    so the RoBERTa model produces a realistic mixed distribution.
    """
    q = query
    raw_comments = [
        # Positive
        f"Absolutely love {q}! This is the best thing to happen in years, totally worth it!",
        f"Wow, {q} just keeps getting better and better. Incredible work from the team!",
        f"I've been following {q} for a long time and this latest update is amazing. So impressed!",
        f"Best decision I ever made was switching to {q}. Highly recommend to everyone!",
        f"{q} is a game changer. Nothing else comes close to this level of quality.",
        f"The innovation coming from {q} is unreal. Excited for what's next!",
        f"Just tried {q} for the first time and it completely blew my mind. 10/10!",
        f"Can't believe how much {q} has improved. The team deserves massive credit.",
        # Negative
        f"Honestly {q} is really disappointing lately. Quality has gone way downhill.",
        f"I hate what {q} has become. Used to be great, now it's just terrible.",
        f"{q} is a scam. Don't waste your money on this garbage.",
        f"Worst experience ever with {q}. Customer service is useless and the product is broken.",
        f"Completely failed with {q}. I'm done. Never again. Total disaster.",
        f"Why does {q} keep making things worse? I'm so frustrated and angry right now.",
        f"Disappointed beyond words with {q}. This is unacceptable and they don't care.",
        f"{q} used to be my favorite but now it's just pure garbage. Very sad.",
        # Neutral / factual
        f"{q} released a new update this week. Changes include several performance improvements.",
        f"Here is a quick overview of {q} and what it does. Make your own decision.",
        f"According to reports, {q} has around 50 million users worldwide as of this year.",
        f"Comparing {q} to similar products: here are the key differences you should know.",
        f"I tested {q} for about two weeks. Here are my observations, both good and bad.",
        f"{q} announced new pricing changes that will take effect next month.",
        f"The latest version of {q} is now available for download on all platforms.",
    ]

    posts = []
    for comment in raw_comments:
        cleaned = clean_text(comment)
        if is_valid_text(cleaned):
            posts.append({"text": comment, "clean_text": cleaned, "platform": "youtube"})
    return posts
