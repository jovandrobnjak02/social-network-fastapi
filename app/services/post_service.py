from aioredis import Redis
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..core.cache import get_cache, set_cache
from ..schemas.response import ResponseMessage
from ..core.enums import ConnectionStatus, Role
from ..db.crud.user import get_connection
from ..schemas.post import Feed, PostInput, PostSchema
from ..db.crud.post import change_post_visibility, delete_post, get_all_posts, get_feed, create_post, get_hidden_posts, get_post, update_post
from ..db.models.user import User

async def get_users_feed(db: Session, current_user: User, redis: Redis):
    key = f"{current_user.username}-feed"
    feed = await get_cache(redis, key)
    
    if feed is None:
        posts = get_feed(db, user_id=current_user.id)
        feed = Feed(posts=posts)
        await set_cache(redis, key, 60, feed.model_dump_json())

    return feed

def add_post(db: Session, post: PostInput, current_user: User):
     post_schema = PostSchema(text = post.text, user_id= current_user.id, image_url= post.image_url)
     return create_post(db, post_schema)

def get_specific_post(db: Session, post_id: int, current_user: User):
    post  = get_post(db, post_id)

    if post.is_hidden and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot get hidden post")
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id = {post_id} not found")
    
    if post.user_id != current_user.id:
        connection = get_connection(db, current_user.id, post.user_id)
        if connection is None or connection["status"] in [ConnectionStatus.NOT_CONNECTED, ConnectionStatus.REQUESTED]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{current_user.username} is not allowed to see the post {post_id}")
        
    return post

def delete_specific_post(db: Session, post_id: int, current_user: User):
    post  = get_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id = {post_id} not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{current_user.username} is not allowed to delete the post {post_id}")
    
    res =delete_post(db, post_id)
    if res:
        return ResponseMessage(msg="Post deleted successfully")
    

def edit_specific_post(db: Session, post_id: int, post: PostInput ,current_user: User):
    existing  = get_post(db, post_id)
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id = {post_id} not found")
    
    if existing.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{current_user.username} is not allowed to delete the post {post_id}")
    
    res =update_post(db, PostSchema(text = post.text, user_id=current_user.id, image_url=post.image_url))
        
    return res


def change_posts_visibility(db: Session, post_id: int,current_user: User, is_hidden):
    existing  = get_post(db, post_id)
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id = {post_id} not found")
    
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Non admin users cant change post visibility")
    
    res = change_post_visibility(db, post_id, is_hidden)
        
    return res


def all_posts(db: Session, current_user: User):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Non admin users cant see all posts")
    
    return get_all_posts(db)

def hidden_posts(db: Session, current_user: User):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Non admin users cant see all posts")
    
    return get_hidden_posts(db)