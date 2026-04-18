from fastapi import APIRouter, Query
from database.mongodb import get_db

router = APIRouter()


@router.get("/posts")
async def get_posts(
    query: str = Query(...),
    platform: str = Query(default=None),
    sentiment: str = Query(default=None),
    limit: int = Query(default=20, le=100),
):
    """Retrieve stored posts for a query with optional filters."""
    db = get_db()
    if db is None:
        return {"posts": [], "total": 0}

    filter_dict = {"query": query.lower()}
    if platform:
        filter_dict["platform"] = platform
    if sentiment:
        filter_dict["sentiment"] = sentiment

    cursor = db.posts.find(filter_dict, {"_id": 0}).limit(limit)
    posts = await cursor.to_list(length=limit)
    total = await db.posts.count_documents(filter_dict)

    return {"posts": posts, "total": total}


@router.get("/history")
async def get_history(limit: int = Query(default=10, le=50)):
    """Get recent analysis queries."""
    db = get_db()
    if db is None:
        return {"history": []}

    cursor = db.analysis_results.find(
        {}, {"_id": 0, "query": 1, "total_posts": 1, "created_at": 1}
    ).sort("created_at", -1).limit(limit)

    history = await cursor.to_list(length=limit)
    return {"history": history}
