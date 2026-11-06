from abc import ABC, abstractmethod

from fastapi import Depends
from sqlalchemy.orm import Session

from src.database import get_db_session
from src.models import Space, User


class ISpaceRepository(ABC):
    @abstractmethod
    def get_spaces_for_user(self, user_id: int) -> list[Space]:
        pass

    @abstractmethod
    def get_space_for_member(self, space_id: int, user_id: int) -> Space | None:
        pass

    @abstractmethod
    def create_space(self, space: Space) -> Space:
        pass

    @abstractmethod
    def delete_space(self, space: Space) -> None:
        pass

    @abstractmethod
    def add_member(self, space: Space, user: User) -> None:
        pass

    @abstractmethod
    def remove_member(self, space: Space, user: User) -> None:
        pass

class SpaceRepository(ISpaceRepository):
    def __init__(self, db_session):
        self.db_session = db_session

    def get_spaces_for_user(self, user_id: int) -> list[Space]:
        return self.db_session.query(Space).join(Space.members).filter(User.id == user_id).all()

    def get_space_for_member(self, space_id: int, user_id: int) -> Space | None:
        return self.db_session.query(Space).join(Space.members).filter(Space.id == space_id, User.id == user_id).first()

    def create_space(self, space: Space) -> Space:
        self.db_session.add(space)
        self.db_session.commit()
        self.db_session.refresh(space)
        return space

    def delete_space(self, space: Space) -> None:
        self.db_session.delete(space)
        self.db_session.commit()

    def add_member(self, space: Space, user: User) -> None:
        space.members.append(user)
        self.db_session.commit()

    def remove_member(self, space: Space, user: User) -> None:
        space.members.remove(user)
        self.db_session.commit()

def get_space_repository(db_session:Session = Depends(get_db_session)) -> ISpaceRepository:
    return SpaceRepository(db_session = db_session)