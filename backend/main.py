from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.database.mongodb import connect_db, disconnect_db
from backend.routes.analyze import router as analyze_router
from backend.routes.posts import router as posts_router


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
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router, prefix="/api", tags=["analyze"])
app.include_router(posts_router, prefix="/api", tags=["posts"])


@app.get("/")
async def root():
    return {"message": "VibeScope API is running", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
