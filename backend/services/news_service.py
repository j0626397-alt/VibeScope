"""
NewsAPI — fetches article titles + descriptions for a keyword.
Falls back to realistic varied mock data when no API key is set.
"""

import os
import asyncio
import aiohttp
from typing import List, Dict
from pipeline.data_cleaning import clean_text, is_valid_text

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
NEWS_API_URL = "https://newsapi.org/v2/everything"


async def fetch_news_posts(query: str, max_posts: int = 50) -> List[Dict]:
    if not NEWS_API_KEY:
        return _mock_news_posts(query)

    params = {
        "q": query,
        "language": "en",
        "pageSize": min(100, max_posts),
        "sortBy": "relevancy",
        "apiKey": NEWS_API_KEY,
    }

    posts = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(NEWS_API_URL, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    return _mock_news_posts(query)
                data = await resp.json()
                for article in data.get("articles", []):
                    title = article.get("title") or ""
                    desc  = article.get("description") or ""
                    # Exact notebook implementation: title + " " + description
                    combined = f"{title} {desc}".strip()
                    cleaned = clean_text(combined)
                    if is_valid_text(cleaned):
                        posts.append({"text": combined, "clean_text": cleaned, "platform": "news"})
    except Exception as e:
        print(f"[News] Error: {e}, using mock data")

    return posts[:max_posts] if posts else _mock_news_posts(query)


def _mock_news_posts(query: str) -> List[Dict]:
    q = query
    raw_articles = [
        # Positive / bullish
        f"{q} Reports Record Revenue Growth, Analysts Raise Price Targets Amid Strong Outlook",
        f"Why {q} Is Winning: Experts Say Leadership and Innovation Are Driving Remarkable Success",
        f"{q} Praised by Industry Leaders for Breakthrough Technology That Sets New Standards",
        f"Investors Love {q}: Stock Surges After Better-Than-Expected Earnings Beat Forecasts",
        f"{q} Expands Globally With New Partnerships, Bringing Exciting Opportunities to Users",
        f"Customers Give {q} Top Marks in Satisfaction Survey, Citing Quality and Reliability",
        f"The Unstoppable Rise of {q}: How It Became the Industry Leader Everyone Admires",
        # Negative / critical
        f"{q} Under Fire: Regulators Launch Formal Investigation Into Data Privacy Violations",
        f"The Troubling Decline of {q}: Users Abandon Platform After Disastrous Policy Changes",
        f"{q} Faces Class Action Lawsuit Over Deceptive Practices, Thousands of Users Affected",
        f"Critics Slam {q} Leadership for Poor Decisions That Have Hurt the Company Badly",
        f"{q} Stock Crashes After Shocking Earnings Miss and Bleak Revenue Guidance Issued",
        f"Former Employees Speak Out Against {q} Culture: 'It Was Toxic and Deeply Dysfunctional'",
        f"Dangerous Flaws Found in {q}: Security Researchers Warn of Serious Vulnerabilities",
        # Neutral / factual
        f"{q} Announces Q3 Earnings Results: Revenue Up Slightly, Margins Remain Under Pressure",
        f"Analysis: {q} Faces Mixed Signals as Market Competition Intensifies Across Sectors",
        f"{q} Releases Annual Report Showing Both Growth Areas and Ongoing Operational Challenges",
        f"Interview: {q} CEO Discusses Strategy, Competition, and Plans for the Coming Year",
        f"{q} Users Divided Over New Features: Some Welcome Changes, Others Express Concerns",
        f"Report: {q} Market Share Holds Steady Despite New Entrants in the Competitive Space",
    ]
    posts = []
    for a in raw_articles:
        cleaned = clean_text(a)
        if is_valid_text(cleaned):
            posts.append({"text": a, "clean_text": cleaned, "platform": "news"})
    return posts
