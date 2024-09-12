from typing import Annotated, List
from aioredis import Redis
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from ..db.models.post import Post
from ..schemas.response import ResponseMessage
from ..schemas.post import ChangeVisibility, Feed, PostInput, PostOut
from ..services.post_service import add_post, all_posts, change_posts_visibility, delete_specific_post, edit_specific_post, get_specific_post, get_users_feed, hidden_posts
from ..dependency import get_db, get_redis
from ..core.security import get_current_active_user
from ..db.models.user import User


router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("/feed")
async def feed(current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db), redis: Redis =  Depends(get_redis)) -> Feed:
    return await get_users_feed(db, current_user, redis)

@router.post("")
def create_post(post: PostInput, current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)) -> PostOut:
    return add_post(db, post, current_user)

@router.get("/{post_id}")
def get_one_post(post_id: Annotated[int, Path(title="The ID of the post to get")], current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)) -> PostOut:
    return get_specific_post(db, post_id, current_user)

@router.delete("/{post_id}")
def delete_one_post(post_id: Annotated[int, Path(title="The ID of the post to delete")], current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)) -> ResponseMessage:
    return delete_specific_post(db, post_id, current_user)

@router.put("/{post_id}")
def edit_one_post(post_id: Annotated[int, Path(title="The ID of the post to delete")],post: PostInput, current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)) -> PostOut:
    return edit_specific_post(db, post_id, post, current_user)

@router.put("/{post_id}/visibility", tags=["admin"])
def change_visibility(post_id: Annotated[int, Path(title="The ID of the post to delete")], data: ChangeVisibility, current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)) -> PostOut:
    return change_posts_visibility(db, post_id, current_user, data.is_hidden)

@router.get("/", tags=["admin"])
def get_all_posts(current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return all_posts(db, current_user)

@router.get("/", tags=["admin"])
def get_hidden_posts(current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return hidden_posts(db, current_user)