from pydantic import BaseModel, Field
from typing import List, Optional , Literal
from datetime import datetime

class Blog(BaseModel):
    title: str
    description: str
    tags: List[str]
    created_at: datetime
    updated_at: Optional[datetime]
    cover_images: List[Optional[str]] = [None, None, None]
    content: str
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