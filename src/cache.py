import redis

from src.config import REDIS_URL

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def get_redis_client() -> redis.Redis:
    return redis_client