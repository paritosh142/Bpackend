import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")

if not mongo_uri or not db_name:
    raise ValueError("MONGO_URI and DB_NAME must be set in the environment variables")

client = AsyncIOMotorClient(mongo_uri)
db = client[db_name]
