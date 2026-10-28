from abc import ABC, abstractmethod

from fastapi import Depends, HTTPException

from src.models import User
from src.repositories.user_repository import IUserRepository, get_user_repository
from src.schemas.user_schema import UserCreate, UserLogin, UserUpdate


class IUserService(ABC):
    @abstractmethod
    def create_user(self, user_data: UserCreate) -> User:
        pass

    @abstractmethod
    def update_user(self, user_id: int, user_data: UserUpdate) -> User | None:
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

    @abstractmethod
    def authenticate_user(self, login_data: UserLogin) -> User:
        pass


class UserService(IUserService):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def create_user(self, user_data: UserCreate) -> User:
        if self.user_repository.get_user_by_username(user_data.username):
            raise HTTPException(status_code=400, detail="Username already exists")

        user = User(username=user_data.username, email=user_data.email)
        user.set_password(user_data.password)
        return self.user_repository.create_user(user)

    def update_user(self, user_id: int, user_data: UserUpdate) -> User | None:
        user = self.user_repository.update_user(user_id, user_data.model_dump(exclude_unset=True))
        if user is None:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} does not exist")
        return user

    def delete_user(self, user_id: int) -> bool:
        if not self.user_repository.delete_user(user_id):
            raise HTTPException(status_code=404, detail=f"User with id {user_id} does not exist")
        return True

    def get_all_users(self) -> list[User]:
        return self.user_repository.get_all_users()

    def get_user_by_username(self, username: str) -> User | None:
        user = self.user_repository.get_user_by_username(username)
        if user is None:
            raise HTTPException(status_code=404, detail=f"User {username} does not exist")
        return user

    def authenticate_user(self, login_data: UserLogin) -> User:
        user = self.user_repository.get_user_by_username(login_data.username)
        if user is None or not user.check_password(login_data.password):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        if not user.is_active:
            raise HTTPException(status_code=403, detail="User is inactive")
        return user
    
def get_user_service(user_repository: IUserRepository = Depends(get_user_repository)) -> IUserService:
       return UserService(user_repository=user_repository)