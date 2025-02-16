import logging
from fastapi import FastAPI, BackgroundTasks, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.routes.blog import router as blog_router
from api.routes.projects import router as project_router
from api.database import db, initialize_counters
from api.email_utils import send_email
import asyncio
import httpx 
from dotenv import load_dotenv
import os 


logging.basicConfig(level=logging.INFO)

app = FastAPI()

load_dotenv()

SMTP_USERNAME = os.getenv("SMTP_USERNAME")

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

@app.post("/send-email")
async def send_email_endpoint(
    background_tasks: BackgroundTasks,
    subject: str = Form(...),
    body: str = Form(...)
):
    recipient = SMTP_USERNAME  
    background_tasks.add_task(send_email, recipient, subject, body)
    return JSONResponse(status_code=200, content={"message": "Email sending initiated"})

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
