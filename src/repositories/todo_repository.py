from abc import ABC, abstractmethod

from fastapi import Depends
from sqlalchemy.orm import Session
from src.database import get_db_session
from src.models import Todo


class ITodoRepository(ABC):

    @abstractmethod
    def get_all_todos(self) -> list[Todo]:
        pass

    @abstractmethod
    def create_todo(self, todo: Todo) -> Todo:
        pass

    @abstractmethod
    def update_todo(self, todo_id: int, data: dict) -> Todo | None:
        pass

    @abstractmethod
    def delete_todo(self, todo_id: int) -> bool:
        pass


class TodoRepository(ITodoRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_todos(self) -> list[Todo]:
        return self.db_session.query(Todo).all()

    def create_todo(self, todo: Todo) -> Todo:
        self.db_session.add(todo)
        self.db_session.commit()
        self.db_session.refresh(todo)
        return todo

    def update_todo(self, todo_id: int, data: dict) -> Todo | None:
        existing_todo = self.db_session.query(Todo).filter(Todo.id == todo_id).first()
        if not existing_todo:
            return None
        for key, value in data.items():
            setattr(existing_todo, key, value)
        self.db_session.commit()
        self.db_session.refresh(existing_todo)
        return existing_todo

    def delete_todo(self, todo_id: int) -> bool:
        existing_todo = self.db_session.query(Todo).filter(Todo.id == todo_id).first()
        if not existing_todo:
            return False
        self.db_session.delete(existing_todo)
        self.db_session.commit()
        return True

def get_todo_repository(db_session: Session = Depends(get_db_session)) -> ITodoRepository:
    return TodoRepository(db_session=db_session)
