from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, UniqueConstraint
from ...core.enums import Role, ConnectionStatus
from sqlalchemy.orm import relationship

from ..base import Base
from .post import Post

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.USER, nullable=False)

    followers = relationship("Connection", 
                             foreign_keys="[Connection.user_id]", 
                             back_populates="followed_user")
    following = relationship("Connection", 
                             foreign_keys="[Connection.follower_id]", 
                             back_populates="follower")
    posts = relationship("Post", foreign_keys="[Post.user_id]", back_populates="owner")

class Connection(Base):
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(ConnectionStatus), nullable=False)

    followed_user = relationship("User", foreign_keys=[user_id], back_populates="followers")
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    __table_args__ = (
        UniqueConstraint('user_id', 'follower_id', name='unique_user_follower_pair'),
    )
