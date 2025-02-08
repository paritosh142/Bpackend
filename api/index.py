from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.blog import router as blog_router
from api.routes.projects import router as project_router
from api.database import db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(blog_router)
app.include_router(project_router)

@app.on_event("startup")
async def startup_db_client():
    await db.command("ping")
    print("Connected to MongoDB!")

# In a serverless environment like Vercel, it's better to leave the connection open
# so that subsequent requests don't attempt to use a closed connection.
# @app.on_event("shutdown")
# async def shutdown_db_client():
#     db.client.close()

@app.get("/")
async def health_check():
    return {"status": "OK"}
