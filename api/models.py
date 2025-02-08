from pydantic import BaseModel
from typing import List, Optional
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
