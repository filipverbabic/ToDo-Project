from abc import ABC, abstractmethod

from fastapi import Depends, HTTPException
from src.repositories.todo_cache_repository import ITodoCacheRepository, get_todo_cache_repository
from src.schemas.todo_schema import TodoCreate, TodoResponse, TodoUpdate
from src.models import Todo
from src.repositories.todo_repository import ITodoRepository, get_todo_repository



class ITodoService(ABC):
    @abstractmethod
    def get_all_todos(self, user_id: int) -> list[Todo]: ...

    @abstractmethod
    def create_todo(self, todo: TodoCreate, user_id: int) -> Todo: ...

    @abstractmethod
    def update_todo(self, todo_id: int, data: TodoUpdate, user_id: int) -> Todo: ...

    @abstractmethod
    def delete_todo(self, todo_id: int, user_id: int) -> None: ...

    @abstractmethod
    def get_space_todos(self, space_id: int) -> list[Todo]: ...

    @abstractmethod
    def create_space_todo(self, space_id: int, todo_data: TodoCreate) -> Todo: ...

    @abstractmethod
    def update_space_todo(self, space_id: int, todo_id: int, todo_data: TodoUpdate) -> Todo: ...

    @abstractmethod
    def delete_space_todo(self, space_id: int, todo_id: int) -> None: ...


class TodoService(ITodoService):
    def __init__(self, todo_repository: ITodoRepository, todo_cache_repository: ITodoCacheRepository):
        self.todo_repository = todo_repository
        self.todo_cache_repository = todo_cache_repository

    def get_all_todos(self, user_id: int) -> list[Todo]:
        cached_todos = self.todo_cache_repository.get_todos(user_id=user_id)
        if cached_todos is not None:
            return [TodoResponse(**todo) for todo in cached_todos]

        
        todos = [TodoResponse.model_validate(todo) for todo in self.todo_repository.get_all_todos(user_id=user_id)]
        self.todo_cache_repository.set_todos(user_id=user_id, todos=[todo.model_dump() for todo in todos])
        return todos

    def create_todo(self, todo_data: TodoCreate, user_id: int) -> Todo:
        todo = self.todo_repository.create_todo(Todo(**todo_data.model_dump(), user_id=user_id))
        self.todo_cache_repository.delete_todos(user_id=user_id)
        return todo

    def update_todo(self, todo_id: int, todo_data: TodoUpdate, user_id: int) -> Todo:
        todo = self.todo_repository.update_todo(todo_id, todo_data.model_dump(exclude_unset=True), user_id)
        if not todo:
            raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
        self.todo_cache_repository.delete_todos(user_id=user_id)
        return todo

    def delete_todo(self, todo_id: int, user_id: int) -> None:
        if not self.todo_repository.delete_todo(todo_id, user_id):
            raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
        self.todo_cache_repository.delete_todos(user_id=user_id)

    def get_space_todos(self, space_id: int) -> list[Todo]:
        cached_todos = self.todo_cache_repository.get_space_todos(space_id=space_id)
        if cached_todos is not None:
            return [TodoResponse(**todo) for todo in cached_todos]

        todos = [TodoResponse.model_validate(todo) for todo in self.todo_repository.get_space_todos(space_id=space_id)]
        self.todo_cache_repository.set_space_todos(space_id=space_id, todos=[todo.model_dump() for todo in todos])
        return todos

    def create_space_todo(self, space_id: int, todo_data: TodoCreate) -> Todo:
        todo = self.todo_repository.create_todo(Todo(**todo_data.model_dump(), space_id=space_id))
        self.todo_cache_repository.delete_space_todos(space_id=space_id)
        return todo

    def update_space_todo(self, space_id: int, todo_id: int, todo_data: TodoUpdate) -> Todo:
        todo = self.todo_repository.update_space_todo(
            todo_id=todo_id,
            data=todo_data.model_dump(exclude_unset=True),
            space_id=space_id,
        )
        if not todo:
            raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
        self.todo_cache_repository.delete_space_todos(space_id=space_id)
        return todo

    def delete_space_todo(self, space_id: int, todo_id: int) -> None:
        if not self.todo_repository.delete_space_todo(todo_id=todo_id, space_id=space_id):
            raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
        self.todo_cache_repository.delete_space_todos(space_id=space_id)

def get_todo_service(todo_repository: ITodoRepository = Depends(get_todo_repository), todo_cache_repository: ITodoCacheRepository = Depends(get_todo_cache_repository)) -> ITodoService:
    return TodoService(todo_repository=todo_repository, todo_cache_repository=todo_cache_repository)