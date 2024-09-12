from typing import List, Optional
from pydantic import BaseModel

from ..core.enums import ConnectionStatus
from .post import PostOut

class UserBase(BaseModel):
    username: str

class UserRegister(UserBase):
    password: str
    first_name: str
    last_name: str
    class Config:
        orm_mode = True

class UserLogin(UserBase):
    password: str

class ConnectionBase(BaseModel):
    username: str
    status: ConnectionStatus

class UserProfile(UserBase):
    id: int
    first_name: str
    last_name: str
    posts: Optional[List[PostOut]]  = []
    connections: Optional[List[ConnectionBase]] = []
    status: Optional[ConnectionStatus] = None

class UserId(BaseModel):
    user_id: int

class UserActivityChange(BaseModel):
    is_active: bool