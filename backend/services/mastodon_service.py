"""
Mastodon public hashtag timeline — no auth required for public posts.
Falls back to realistic varied mock data when API is unreachable.
"""

import os
import asyncio
import aiohttp
from typing import List, Dict
from bs4 import BeautifulSoup
from backend.pipeline.data_cleaning import clean_text, is_valid_text

MASTODON_INSTANCE = "https://mastodon.social"
MASTODON_TOKEN = os.getenv("MASTODON_TOKEN", "")


async def fetch_mastodon_posts(query: str, max_posts: int = 50) -> List[Dict]:
    hashtag = query.replace(" ", "").replace("#", "").strip()
    posts = []

    headers = {}
    if MASTODON_TOKEN:
        headers["Authorization"] = f"Bearer {MASTODON_TOKEN}"

    url = f"{MASTODON_INSTANCE}/api/v1/timelines/tag/{hashtag}?limit=40"

    try:
        async with aiohttp.ClientSession() as session:
            for _ in range(5):
                if len(posts) >= max_posts:
                    break
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status != 200:
                        break
                    data = await resp.json()
                    if not data:
                        break
                    for post in data:
                        raw_html = post.get("content", "")
                        plain = BeautifulSoup(raw_html, "html.parser").get_text()
                        cleaned = clean_text(plain)
                        if is_valid_text(cleaned):
                            posts.append({"text": plain, "clean_text": cleaned, "platform": "mastodon"})
                    last_id = data[-1]["id"]
                    url = f"{MASTODON_INSTANCE}/api/v1/timelines/tag/{hashtag}?limit=40&max_id={last_id}"
    except Exception as e:
        print(f"[Mastodon] Error: {e}, using mock data")

    return posts[:max_posts] if posts else _mock_mastodon_posts(query)


def _mock_mastodon_posts(query: str) -> List[Dict]:
    q = query
    raw_posts = [
        # Positive
        f"Really loving {q} right now. The community around it is so supportive and vibrant!",
        f"Huge fan of everything {q} is doing. This is exactly the innovation we needed.",
        f"{q} just announced something incredible. This is going to change everything for the better!",
        f"So happy with {q}. It exceeded all my expectations and more. Absolutely wonderful.",
        f"The progress {q} is making is inspiring. Great to see such positive momentum.",
        f"I switched to {q} last month and honestly my life is better. No regrets whatsoever.",
        f"Delighted by the latest {q} release. The team really listened to user feedback!",
        # Negative
        f"I am so frustrated with {q} right now. This is unacceptable and I am done.",
        f"Why is {q} getting worse? It used to be great. Now it's just broken and terrible.",
        f"Concerned about the privacy issues with {q}. This is a serious problem. Very bad.",
        f"Angry at {q} for the recent changes. Nobody asked for this and it ruined everything.",
        f"{q} keeps disappointing me. I expected better and they delivered garbage. Terrible.",
        f"The decline of {q} is so sad to watch. What a terrible direction they're heading.",
        # Neutral
        f"{q} released version 3.0 today. Here are the key changes listed in the changelog.",
        f"Just read about {q}. Has both advantages and disadvantages depending on your use case.",
        f"Has anyone else been following the {q} situation? Would love to hear different perspectives.",
        f"{q} is growing its user base. Latest numbers show steady adoption across regions.",
        f"Interesting article about {q} and how it compares to alternatives in the market.",
    ]
    posts = []
    for p in raw_posts:
        cleaned = clean_text(p)
        if is_valid_text(cleaned):
            posts.append({"text": p, "clean_text": cleaned, "platform": "mastodon"})
    return posts
