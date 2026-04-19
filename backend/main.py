from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.database.mongodb import connect_db, disconnect_db
from backend.routes.analyze import router as analyze_router
from backend.routes.posts import router as posts_router

import os
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await disconnect_db()


app = FastAPI(
    title="VibeScope API",
    description="Social Media Sentiment Analysis Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://vibe-scope-two.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router, prefix="/api", tags=["analyze"])
app.include_router(posts_router, prefix="/api", tags=["posts"])

@app.on_event("startup")
async def preload_models():
    print("Loading ML models...")

    from ml_service.sentiment_model import _load_model
    _load_model()

    from ml_service.emotion_detector import _load_emotion_pipeline
    _load_emotion_pipeline()

    print("Models loaded successfully")

@app.get("/")
async def root():
    return {"message": "VibeScope API is running", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)