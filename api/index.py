import logging
from fastapi import FastAPI , BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from api.routes.blog import router as blog_router
from api.routes.projects import router as project_router
from api.database import db, initialize_counters
import asyncio
import httpx 

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(blog_router)
app.include_router(project_router)

@app.get("/ping")
async def ping():
    return {"status": "alive"}

async def keep_alive():
    async with httpx.AsyncClient() as client:
        while True:
            try:
                response = await client.get("https://bpackend.onrender.com/ping")
                logging.info(f"Keep-alive ping sent. Status: {response.status_code}")
            except Exception as e:
                logging.error(f"Keep-alive ping failed: {str(e)}")
            await asyncio.sleep(300)  # Wait for 5 minutes before the next ping

@app.on_event("startup")
async def start_keep_alive():
    logging.info("Starting keep-alive task and initializing counters...")
    asyncio.create_task(keep_alive())
    await initialize_counters(app)  # Ensure counters are initialized

@app.get("/")
async def health_check():
    return {"status": "OK"}
