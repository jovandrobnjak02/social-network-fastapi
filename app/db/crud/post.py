from sqlalchemy import desc
from sqlalchemy.orm import Session
from ...schemas.post import PostOut, PostSchema
from ..models.user import Connection
from ..models.post import Post

def get_feed(db: Session, user_id: int):
    connection_user_ids = db.query(Connection.user_id).filter(Connection.follower_id == user_id).all()
    follower_user_ids = db.query(Connection.follower_id).filter(Connection.user_id == user_id).all()

    user_ids = {id for (id,) in connection_user_ids + follower_user_ids}
    feed_posts = db.query(Post).filter(Post.user_id.in_(user_ids) & Post.is_hidden == False).order_by(desc(Post.posted_at)).all()

    return feed_posts

def get_users_posts(db: Session, user_id: int):
    return db.query(Post).filter(Post.user_id == user_id).order_by(desc(Post.posted_at)).all()

def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).order_by(desc(Post.posted_at)).one_or_none()

def get_all_posts(db: Session):
    return db.query(Post).all()

def get_hidden_posts(db: Session):
    return db.query(Post).filter(Post.is_hidden == True).all()

def create_post(db: Session, post: PostSchema):
    db_post = Post(text = post.text, user_id = post.user_id, image_url = post.image_url)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post: PostSchema):
    db_post = db.query(Post).filter(Post.id == post.id).first()
    if db_post:
        db_post.image_url = post.image_url
        db_post.text = post.text
        db.commit()
        db.refresh(db_post)

    return db_post

def change_post_visibility(db: Session, post_id: int, is_hidden: bool):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        db_post.is_hidden = is_hidden
        db.commit()
        db.refresh(db_post)

    return db_post

def delete_post(db: Session, post_id: int):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
    return True