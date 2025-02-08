from fastapi import FastAPI
from api.database import db
from api.routes.blog import router as blog_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(blog_router)


@app.get("/")
async def health_check():
    return {"status": "OK"}