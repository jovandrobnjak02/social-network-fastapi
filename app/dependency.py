from .db.base import SessionLocal
from .core.cache import client

def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_redis():
    redis = client
    try:
        yield redis
    finally:
        await redis.close()