from fastapi import FastAPI , BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from api.routes.blog import router as blog_router
from api.routes.projects import router as project_router
from api.database import db
import asyncio
import httpx

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
                print(f"Keep-alive ping sent. Status: {response.status_code}")
            except Exception as e:
                print(f"Keep-alive ping failed: {str(e)}")
            await asyncio.sleep(300)  # Wait for 5 minutes before the next ping

@app.on_event("startup")
async def start_keep_alive():
    asyncio.create_task(keep_alive())
@app.get("/")
async def health_check():
    return {"status": "OK"}
