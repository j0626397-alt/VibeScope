"""
Seed MongoDB with sample VibeScope data for development/testing.
Run: python database/seed_data.py
"""
import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

SAMPLE_ANALYSIS = {
    "query": "openai",
    "sentiment_distribution": {"positive": 54.2, "neutral": 28.1, "negative": 17.7},
    "platform_sentiment": {
        "youtube": {"positive": 62.0, "neutral": 22.0, "negative": 16.0},
        "mastodon": {"positive": 41.0, "neutral": 35.0, "negative": 24.0},
        "news": {"positive": 55.0, "neutral": 30.0, "negative": 15.0},
        "hackernews": {"positive": 49.0, "neutral": 28.0, "negative": 23.0},
    },
    "emotion_distribution": {
        "happy": 32.5,
        "excitement": 28.1,
        "neutral": 22.4,
        "anger": 10.3,
        "sadness": 6.7,
    },
    "trending_keywords": [
        "gpt", "model", "chatgpt", "api", "ai", "reasoning", "agents", "safety", "llm", "research"
    ],
    "wordcloud_data": {
        "gpt": 120, "model": 95, "ai": 88, "chatgpt": 82, "openai": 75,
        "reasoning": 60, "agents": 55, "llm": 50, "api": 48, "safety": 44,
        "research": 40, "future": 38, "technology": 35, "intelligence": 33,
        "training": 30, "data": 28, "performance": 25, "powerful": 22,
    },
    "example_posts": {
        "positive": "OpenAI's latest model is genuinely impressive. The reasoning capabilities have improved dramatically.",
        "neutral": "OpenAI released new API pricing. Changes take effect next month for all tiers.",
        "negative": "Concerned about the direction OpenAI is taking. Feels less open-source focused than ever.",
    },
    "summary": (
        "Public sentiment around OpenAI is largely positive, with users praising the advanced reasoning "
        "capabilities and model improvements. Excitement around AI agents and GPT developments drives "
        "enthusiasm, while some concerns persist around safety practices and openness."
    ),
    "total_posts": 192,
    "created_at": datetime.utcnow(),
}


async def seed():
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client["vibescope"]

    # Clear existing seed
    await db.analysis_results.delete_many({"query": "openai"})

    # Insert sample
    await db.analysis_results.insert_one(SAMPLE_ANALYSIS)
    print("[Seed] Inserted sample analysis for 'openai'")

    # Create indexes
    await db.analysis_results.create_index([("query", 1), ("created_at", -1)])
    await db.posts.create_index([("query", 1), ("platform", 1), ("sentiment", 1)])
    print("[Seed] Indexes created")

    client.close()
    print("[Seed] Done!")


if __name__ == "__main__":
    asyncio.run(seed())
