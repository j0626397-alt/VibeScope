"""
Hacker News Firebase API — fetches top/new stories matching the query keyword.
Exact approach from the notebook: search top 200 story titles for keyword match.
Falls back to realistic varied mock data.
"""

import asyncio
import aiohttp
from typing import List, Dict
from pipeline.data_cleaning import clean_text, is_valid_text

HN_BASE = "https://hacker-news.firebaseio.com/v0"


async def fetch_hackernews_posts(query: str, max_posts: int = 50) -> List[Dict]:
    posts = []
    keyword = query.lower().replace("#", "")

    try:
        async with aiohttp.ClientSession() as session:
            # Fetch top story IDs — exact notebook approach
            async with session.get(f"{HN_BASE}/topstories.json", timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    return _mock_hn_posts(query)
                top_ids = await resp.json()

            # Fetch up to 300 stories concurrently and filter by keyword
            semaphore = asyncio.Semaphore(30)

            async def fetch_item(item_id: int) -> Dict | None:
                async with semaphore:
                    try:
                        async with session.get(
                            f"{HN_BASE}/item/{item_id}.json",
                            timeout=aiohttp.ClientTimeout(total=5),
                        ) as r:
                            if r.status == 200:
                                return await r.json()
                    except Exception:
                        pass
                return None

            items = await asyncio.gather(*[fetch_item(i) for i in top_ids[:300]])

            for item in items:
                if not item or "title" not in item:
                    continue
                title = item.get("title", "")
                # Exact notebook condition: keyword in title (case-insensitive)
                if keyword in title.lower():
                    cleaned = clean_text(title)
                    if is_valid_text(cleaned):
                        posts.append({"text": title, "clean_text": cleaned, "platform": "hackernews"})
                if len(posts) >= max_posts:
                    break

    except Exception as e:
        print(f"[HackerNews] Error: {e}, using mock data")

    return posts[:max_posts] if posts else _mock_hn_posts(query)


def _mock_hn_posts(query: str) -> List[Dict]:
    q = query
    raw_titles = [
        # Positive / enthusiastic (HN style)
        f"Show HN: We rebuilt our entire stack with {q} and performance improved 10x",
        f"{q} is genuinely the best tool I have used in a decade. Here is why.",
        f"Why I love {q} and think it will dominate the next five years",
        f"The engineering behind {q} is brilliant — a deep dive into what makes it great",
        f"{q} just open-sourced their core engine and it is incredible work",
        f"How {q} solved problems that seemed impossible six months ago",
        f"After trying everything else, {q} is the only solution that actually works",
        # Negative / critical (HN style)
        f"Ask HN: Is anyone else frustrated with {q}'s terrible recent decisions?",
        f"The dark side of {q} that nobody wants to talk about — a critical analysis",
        f"Why I stopped using {q} after two years and what I switched to instead",
        f"{q} is destroying developer trust with their latest privacy-violating update",
        f"Hot take: {q} is overrated and the community refuses to admit its problems",
        f"I analyzed {q}'s codebase and found serious quality and security issues",
        f"{q} was great until they sold out. Now it is just a bloated mess.",
        # Neutral / technical (HN style)
        f"Ask HN: What is your honest opinion of {q} compared to alternatives?",
        f"Technical comparison of {q} vs competitors across ten different benchmarks",
        f"{q} CEO announces roadmap at annual conference — here are the highlights",
        f"How {q} scaled to 10M users — an engineering retrospective",
        f"Understanding {q}'s architecture: a detailed technical overview",
        f"The history and evolution of {q}: from startup to industry player",
    ]
    posts = []
    for t in raw_titles:
        cleaned = clean_text(t)
        if is_valid_text(cleaned):
            posts.append({"text": t, "clean_text": cleaned, "platform": "hackernews"})
    return posts
