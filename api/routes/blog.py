from fastapi import APIRouter, HTTPException
from api.database import db
from api.models import Blog
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/blogs", tags=["blog"])

@router.get("/", response_model=list[dict])
async def get_blogs():
    blogs = []
    async for blog in db.blogs.find():
        blog['_id'] = str(blog['_id'])
        blogs.append(blog)
    return blogs

@router.post("/", response_model=Blog)
async def add_blog(blog: Blog):
    blog_data = blog.dict()
    blog_data['created_at'] = datetime.utcnow()
    blog_data['updated_at'] = None
    await db.blogs.insert_one(blog_data)
    return blog

@router.get("/{blog_id}", response_model=dict)
async def get_blog(blog_id: str):
    blog = await db.blogs.find_one({"_id": ObjectId(blog_id)})
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog['_id'] = str(blog['_id'])
    return blog

@router.put("/{blog_id}", response_model=Blog)
async def update_blog(blog_id: str, blog: Blog):
    blog_data = blog.dict()
    blog_data['updated_at'] = datetime.utcnow()
    result = await db.blogs.update_one({"_id": ObjectId(blog_id)}, {"$set": blog_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.delete("/{blog_id}", response_model=dict)
async def delete_blog(blog_id: str):
    result = await db.blogs.delete_one({"_id": ObjectId(blog_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted successfully"}

@router.get("/frontend-url", response_model=dict)
async def get_frontend_url():
    return {"url": "https://byteupp.vercel.app/"}
