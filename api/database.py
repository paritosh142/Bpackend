import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from fastapi import FastAPI
from datetime import datetime
import logging

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")

if not mongo_uri or not db_name:
    raise ValueError("MONGO_URI and DB_NAME must be set in the environment variables")

client = AsyncIOMotorClient(mongo_uri)
db = client[db_name]

async def initialize_counters(app: FastAPI):
    logging.info("Initializing counters...")
    counter = await db.counters.find_one({"_id": "blog_id"})
    if not counter:
        logging.info("Counter document not found. Creating a new one.")
        await db.counters.insert_one({
            "_id": "blog_id",
            "seq": 0,
            "created_at": datetime.utcnow()
        })
    else:
        logging.info("Counter document already exists.")