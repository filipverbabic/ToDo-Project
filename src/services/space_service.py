from abc import ABC, abstractmethod

from fastapi import Depends, HTTPException

from src.models import Space, User
from src.repositories.space_repository import ISpaceRepository, get_space_repository
from src.schemas.space_schema import SpaceCreate
from src.services.security_service import get_current_user
from src.services.user_service import IUserService, get_user_service


class ISpaceService(ABC):
    @abstractmethod
    def get_my_spaces(self, user_id: int) -> list[Space]: ...

    @abstractmethod
    def create_space(self, space_data: SpaceCreate, user: User) -> Space: ...

    @abstractmethod
    def get_space_for_member(self, space_id: int, user_id: int) -> Space: ...

    @abstractmethod
    def delete_space(self, space: Space) -> None: ...

    @abstractmethod
    def get_space_members(self, space: Space) -> list[User]: ...

    @abstractmethod
    def add_member(self, space: Space, username: str) -> None: ...

    @abstractmethod
    def remove_member(self, space: Space, user_id: int) -> None: ...


class SpaceService(ISpaceService):
    def __init__(self, space_repository: ISpaceRepository, user_service: IUserService):
        self.space_repository = space_repository
        self.user_service = user_service

    def get_my_spaces(self, user_id: int) -> list[Space]:
        return self.space_repository.get_spaces_for_user(user_id)

    def create_space(self, space_data: SpaceCreate, user: User) -> Space:
        new_space = Space(**space_data.model_dump())
        new_space.members.append(user)
        return self.space_repository.create_space(new_space)

    def get_space_for_member(self, space_id: int, user_id: int) -> Space:
        space = self.space_repository.get_space_for_member(space_id, user_id)
        if not space:
            raise HTTPException(status_code=404, detail=f"Space with id '{space_id}' not found.")
        return space

    def delete_space(self, space: Space) -> None:
        self.space_repository.delete_space(space)

    def get_space_members(self, space: Space) -> list[User]:
        return space.members

    def add_member(self, space: Space, username: str) -> None:
        user = self.user_service.get_user_by_username(username)
        if user in space.members:
            raise HTTPException(status_code=409, detail=f"User with username '{username}' is already a member of the space.")
        self.space_repository.add_member(space, user)

    def remove_member(self, space: Space, user_id: int) -> None:
        user = self.user_service.get_user_by_id(user_id)
        if user not in space.members:
            raise HTTPException(status_code=404, detail=f"User with id '{user_id}' is not a member of the space.")
        self.space_repository.remove_member(space, user)
        if not space.members:
            self.space_repository.delete_space(space)

def get_space_service(space_repository: ISpaceRepository = Depends(get_space_repository), user_service: IUserService = Depends(get_user_service)) -> ISpaceService:
    return SpaceService(space_repository=space_repository, user_service=user_service)

def get_member_space(space_id: int, current_user: User = Depends(get_current_user), space_service: ISpaceService = Depends(get_space_service)) -> Space:
    return space_service.get_space_for_member(space_id, current_user.id)