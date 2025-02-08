import os 
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")

# Debugging print statements
print(f"MONGO_URI: {mongo_uri}")
print(f"DB_NAME: {db_name}")

if not mongo_uri or not db_name:
	raise ValueError("MONGO_URI and DB_NAME must be set in the environment variables")

client = AsyncIOMotorClient(mongo_uri)
db = client[db_name]