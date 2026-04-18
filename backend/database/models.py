from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PostModel(BaseModel):
    text: str
    clean_text: str
    platform: str  # youtube | mastodon | news | hackernews
    sentiment: str  # positive | neutral | negative
    emotion: str    # happy | anger | sadness | excitement | neutral
    score: Optional[float] = None
    query: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    source_date: Optional[str] = None


class AnalysisResultModel(BaseModel):
    query: str
    sentiment_distribution: dict
    platform_sentiment: dict
    emotion_distribution: dict
    trending_keywords: List[str]
    wordcloud_data: dict
    example_posts: dict
    summary: str
    total_posts: int
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AnalyzeRequest(BaseModel):
    query: str


class AnalyzeResponse(BaseModel):
    query: str
    sentiment_distribution: dict
    platform_sentiment: dict
    emotion_distribution: dict
    trending_keywords: List[str]
    wordcloud_data: dict
    example_posts: dict
    summary: str
    total_posts: int
    cached: bool = False
