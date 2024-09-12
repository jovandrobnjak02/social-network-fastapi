from aioredis import Redis, from_url
from json import dumps, loads
from .config import settings

REDIS_URL = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
client = from_url(REDIS_URL)

async def set_cache(redis: Redis, key: str, expire: int, value):
    await redis.set(key, value, ex= expire)


async def get_cache(redis: Redis, key: str):
    value = await redis.get(key)
    if value:
        return loads(value)
    
    else:
        return None