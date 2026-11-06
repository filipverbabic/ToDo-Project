from functools import wraps
import json

from fastapi.encoders import jsonable_encoder
import redis

from src.config import REDIS_URL

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def get_redis_client() -> redis.Redis:
    return redis_client

def cache_response(key_prefix: str, ttl: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = kwargs["current_user"]
            key = f"{key_prefix}:user:{current_user.id}"

            cached_response = redis_client.get(key)
            if cached_response is not None:
                return json.loads(cached_response)
            response = func(*args, **kwargs)
            redis_client.set(key, json.dumps(jsonable_encoder(response)), ex=ttl)
            return response
        return wrapper
    return decorator