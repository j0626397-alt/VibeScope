import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = "vibescope"

client: AsyncIOMotorClient = None
db = None


async def connect_db():
    global client, db
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    print(f"[MongoDB] Connected to {DB_NAME}")


async def disconnect_db():
    global client
    if client:
        client.close()
        print("[MongoDB] Disconnected")


def get_db():
    return db
