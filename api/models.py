from pydantic import BaseModel, Field
from typing import List, Optional , Literal
from datetime import datetime

class BlogBase(BaseModel):
    title: str
    description: str
    tags: List[str]
    content: str
    cover_images: List[Optional[str]] = Field(
        [None, None, None], 
        max_items=3,
        description="Max 3 cover images"
    )

class BlogCreate(BlogBase):
    pass

class Blog(BlogBase):
    blog_id: int = Field(..., ge=1, le=50)  
    created_at: datetime
    updated_at: Optional[datetime] = None
    views: int = 0

class ProjectLinks(BaseModel):
    live: Optional[str] = None
    repo: Optional[str] = None
    case_study: Optional[str] = None

class ProjectBase(BaseModel):
    title: str
    type: Literal["web", "mobile", "saas", "ai"]
    industry: str
    description: str
    tech_stack: list[str] = Field(..., min_items=1)
    metrics: dict[str, str]
    images: list[str] = Field(..., max_items=3)
    links: Optional[ProjectLinks] = None