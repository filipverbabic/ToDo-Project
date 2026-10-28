from abc import ABC, abstractmethod

from fastapi import Depends
from sqlalchemy.orm import Session
from src.database import get_db_session
from src.models import User


class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def update_user(self, user_id: int, user_data: dict) -> User | None:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def get_all_users(self) -> list[User]:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> User | None:
        pass


class UserRepository(IUserRepository):
    def __init__(self, db_session):
        self.db_session = db_session
        

    def create_user(self, user: User) -> User:
        self.db_session.add(user)
        self.db_session.commit()
        return user

    def update_user(self, user_id: int, user_data: dict) -> User | None:
        existing_user = self.db_session.query(User).filter(User.id == user_id).first()
        if not existing_user:
            return None
        for key, value in user_data.items():
            setattr(existing_user, key, value)
        self.db_session.commit()
        self.db_session.refresh(existing_user)
        return existing_user

    def delete_user(self, user_id: int) -> bool:
        existing_user = self.db_session.query(User).filter(User.id == user_id).first()
        if not existing_user:
            return False
        self.db_session.delete(existing_user)
        self.db_session.commit()
        return True

    def get_all_users(self) -> list[User]:
        return self.db_session.query(User).all()

    def get_user_by_username(self, username: str) -> User | None:
        return self.db_session.query(User).filter(User.username == username).first()

def get_user_repository(db_session: Session = Depends(get_db_session)) -> IUserRepository:
    return UserRepository(db_session=db_session)