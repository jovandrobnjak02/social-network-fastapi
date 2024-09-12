from fastapi import FastAPI
from .db.base import Base, engine
from .routers import auth, user, post
from .core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router, prefix=settings.API_VERSION)
app.include_router(user.router, prefix=settings.API_VERSION)
app.include_router(post.router, prefix=settings.API_VERSION)