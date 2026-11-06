
from abc import ABC, abstractmethod
import json

from fastapi import Depends
from redis import Redis

from src.cache import get_redis_client

CACHE_TTL_SECONDS = 60


class ITodoCacheRepository(ABC):
    @abstractmethod
    def get_todos(self, user_id: int) -> list[dict] | None: ...

    @abstractmethod
    def set_todos(self, user_id: int, todos: list[dict]) -> None: ...

    @abstractmethod
    def delete_todos(self, user_id: int) -> None: ...

    @abstractmethod
    def get_space_todos(self, space_id: int) -> list[dict] | None: ...

    @abstractmethod
    def set_space_todos(self, space_id: int, todos: list[dict]) -> None: ...

    @abstractmethod
    def delete_space_todos(self, space_id: int) -> None: ...


class TodoCacheRepository(ITodoCacheRepository):

    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def _get_key(self, user_id: int) -> str:
        return f"todos:user:{user_id}"

    def _get_space_key(self, space_id: int) -> str:
        return f"todos:space:{space_id}"

    def get_todos(self, user_id: int):
        cached_todos = self.redis_client.get(self._get_key(user_id))
        if not cached_todos:
            return None
        return json.loads(cached_todos)

    def set_todos(self, user_id: int, todos: list[dict]):
        self.redis_client.set(self._get_key(user_id), json.dumps(todos), ex=CACHE_TTL_SECONDS)

    def delete_todos(self, user_id: int):
        self.redis_client.delete(self._get_key(user_id))

    def get_space_todos(self, space_id: int):
        cached_todos = self.redis_client.get(self._get_space_key(space_id))
        if not cached_todos:
            return None
        return json.loads(cached_todos)

    def set_space_todos(self, space_id: int, todos: list[dict]):
        self.redis_client.set(self._get_space_key(space_id), json.dumps(todos), ex=CACHE_TTL_SECONDS)

    def delete_space_todos(self, space_id: int):
        self.redis_client.delete(self._get_space_key(space_id))


def get_todo_cache_repository(redis_client: Redis = Depends(get_redis_client)) -> ITodoCacheRepository:
    return TodoCacheRepository(redis_client=redis_client)