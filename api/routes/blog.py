from fastapi import APIRouter, HTTPException, Query, Path
from api.database import db
from api.models import Blog, BlogCreate
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/blogs", tags=["blogs"])

def get_cyclic_id(sequence: int) -> int:
    return (sequence % 50) or 50  # Returns 1-50

@router.post("/", response_model=Blog)
async def create_blog(blog: BlogCreate):
    # 1. Get current sequence number
    counter = await db.counters.find_one_and_update(
        {"_id": "blog_id"},
        {"$inc": {"seq": 1}},
        return_document=True
    )
    
    # 2. Calculate cyclic ID
    current_blog_id = get_cyclic_id(counter['seq'])
    
    # 3. Delete existing blog with this ID if exists
    existing_blog = await db.blogs.find_one({"blog_id": current_blog_id})
    if existing_blog:
        await db.blogs.delete_one({"blog_id": current_blog_id})
    
    # 4. Create new blog document
    blog_data = blog.dict()
    blog_data.update({
        "blog_id": current_blog_id,
        "created_at": datetime.utcnow(),
        "updated_at": None,
        "views": 0
    })
    
    # 5. Insert new blog
    result = await db.blogs.insert_one(blog_data)
    
    # 6. Return created blog
    new_blog = await db.blogs.find_one({"_id": result.inserted_id})
    new_blog["_id"] = str(new_blog["_id"])
    return new_blog

@router.get("/{blog_id}", response_model=Blog)
async def get_blog(blog_id: int = Path(..., ge=1, le=50)):
    blog = await db.blogs.find_one({"blog_id": blog_id})
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog["_id"] = str(blog["_id"])
    return blog

@router.get("/", response_model=list[dict])
async def get_blogs():
    blogs = []
    async for blog in db.blogs.find():
        blog['_id'] = str(blog['_id'])
        blogs.append(blog)
    return blogs

@router.put("/{blog_id}", response_model=Blog)
async def update_blog(blog_id: int, blog: BlogCreate):
    blog_data = blog.dict()
    blog_data['updated_at'] = datetime.utcnow()
    result = await db.blogs.update_one({"blog_id": blog_id}, {"$set": blog_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    updated_blog = await db.blogs.find_one({"blog_id": blog_id})
    updated_blog["_id"] = str(updated_blog["_id"])
    return updated_blog

@router.delete("/{blog_id}", response_model=dict)
async def delete_blog(blog_id: int = Path(..., ge=1, le=50)):
    result = await db.blogs.delete_one({"blog_id": blog_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted successfully"}

@router.get("/{blog_id}/other-blogs", response_model=list[dict])
async def get_random_other_blogs(
    blog_id: int = Path(..., ge=1, le=50),
    limit: int = Query(2, description="Number of random blogs to return", ge=1, le=10)
):
    # Check if the blog exists
    blog = await db.blogs.find_one({"blog_id": blog_id})
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    # Get random blogs excluding the current one
    pipeline = [
        {
            "$match": {
                "blog_id": {"$ne": blog_id}  # Exclude current blog
            }
        },
        {
            "$sample": {"size": limit}  # Random selection
        }
    ]

    random_blogs = []
    async for doc in db.blogs.aggregate(pipeline):
        doc['_id'] = str(doc['_id'])
        random_blogs.append(doc)

    return random_blogs