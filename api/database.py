import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from fastapi import FastAPI
from datetime import datetime

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")

if not mongo_uri or not db_name:
    raise ValueError("MONGO_URI and DB_NAME must be set in the environment variables")

client = AsyncIOMotorClient(mongo_uri)
db = client[db_name]

async def initialize_counters(app: FastAPI):
    # Create blog_id counter if not exists
    if await db.counters.find_one({"_id": "blog_id"}) is None:
        await db.counters.insert_one({
            "_id": "blog_id",
            "seq": 0,
            "created_at": datetime.utcnow()
        })