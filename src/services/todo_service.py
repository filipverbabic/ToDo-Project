from abc import ABC, abstractmethod

from fastapi import Depends, HTTPException

from src.schemas.todo_schema import TodoCreate, TodoUpdate
from src.models import Todo
from src.repositories.todo_repository import ITodoRepository, get_todo_repository


class ITodoService(ABC):
    @abstractmethod
    def get_all_todos(self) -> list[Todo]: ...

    @abstractmethod
    def create_todo(self, todo: Todo) -> Todo: ...

    @abstractmethod
    def update_todo(self, todo_id: int, data: dict) -> Todo: ...

    @abstractmethod
    def delete_todo(self, todo_id: int) -> None: ...


class TodoService(ITodoService):
    def __init__(self, todo_repository: ITodoRepository):
        self.todo_repository = todo_repository

    def get_all_todos(self) -> list[Todo]:
        return self.todo_repository.get_all_todos()

    def create_todo(self, todo_data: TodoCreate) -> Todo:
        return self.todo_repository.create_todo(Todo(**todo_data.model_dump()))

    def update_todo(self, todo_id: int, todo_data: TodoUpdate) -> Todo:
        todo = self.todo_repository.update_todo(todo_id, todo_data.model_dump(exclude_unset=True))
        if not todo:
            raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
        return todo

    def delete_todo(self, todo_id: int) -> None:
        if not self.todo_repository.delete_todo(todo_id):
            raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")

def get_todo_service(todo_repository: ITodoRepository = Depends(get_todo_repository)) -> ITodoService:
    return TodoService(todo_repository=todo_repository)