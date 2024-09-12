from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class PostBase(BaseModel):
    text : str
    user_id: int
    

class PostSchema(PostBase):
    image_url: str = ""
    class Config:
        orm_mode = True

class PostOut(PostBase):
    id: int
    image_url: str = ""
    posted_at: datetime
    class Config:
        orm_mode = True
        from_attributes=True

class Feed(BaseModel):
    posts: List[PostOut] = []

class PostInput(BaseModel):
    text : str
    image_url: Optional[str] = ""

class ChangeVisibility(BaseModel):
    is_hidden: bool