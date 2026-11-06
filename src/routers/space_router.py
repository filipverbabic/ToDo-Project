from fastapi import APIRouter, Depends

from src.models import Space, User
from src.schemas.space_schema import SpaceCreate, SpaceMemberAdd, SpaceMemberResponse, SpaceResponse
from src.schemas.todo_schema import TodoCreate, TodoResponse, TodoUpdate
from src.services.security_service import get_current_user
from src.services.space_service import ISpaceService, get_member_space, get_space_service
from src.services.todo_service import ITodoService, get_todo_service


router = APIRouter(prefix="/spaces", tags=["Spaces"])


@router.get("", response_model=list[SpaceResponse])
def get_my_spaces(
    current_user: User = Depends(get_current_user),
    space_service: ISpaceService = Depends(get_space_service),
):
    return space_service.get_my_spaces(user_id=current_user.id)


@router.post("", status_code=201, response_model=SpaceResponse)
def create_space(
    space_data: SpaceCreate,
    current_user: User = Depends(get_current_user),
    space_service: ISpaceService = Depends(get_space_service),
):
    return space_service.create_space(space_data=space_data, user=current_user)


@router.delete("/{space_id}", status_code=204)
def delete_space(
    space: Space = Depends(get_member_space),
    space_service: ISpaceService = Depends(get_space_service),
):
    space_service.delete_space(space=space)


@router.get("/{space_id}/members", response_model=list[SpaceMemberResponse])
def get_space_members(
    space: Space = Depends(get_member_space),
    space_service: ISpaceService = Depends(get_space_service),
):
    return space_service.get_space_members(space=space)


@router.post("/{space_id}/members", status_code=204)
def add_member(
    member_data: SpaceMemberAdd,
    space: Space = Depends(get_member_space),
    space_service: ISpaceService = Depends(get_space_service),
):
    space_service.add_member(space=space, username=member_data.username)


@router.delete("/{space_id}/members/{user_id}", status_code=204)
def remove_member(
    user_id: int,
    space: Space = Depends(get_member_space),
    space_service: ISpaceService = Depends(get_space_service),
):
    space_service.remove_member(space=space, user_id=user_id)


@router.get("/{space_id}/todos", response_model=list[TodoResponse])
def get_space_todos(
    space: Space = Depends(get_member_space),
    todo_service: ITodoService = Depends(get_todo_service),
):
    return todo_service.get_space_todos(space_id=space.id)


@router.post("/{space_id}/todos", status_code=201, response_model=TodoResponse)
def create_space_todo(
    todo_data: TodoCreate,
    space: Space = Depends(get_member_space),
    todo_service: ITodoService = Depends(get_todo_service),
):
    return todo_service.create_space_todo(space_id=space.id, todo_data=todo_data)


@router.patch("/{space_id}/todos/{todo_id}", response_model=TodoResponse)
def update_space_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    space: Space = Depends(get_member_space),
    todo_service: ITodoService = Depends(get_todo_service),
):
    return todo_service.update_space_todo(space_id=space.id, todo_id=todo_id, todo_data=todo_data)


@router.delete("/{space_id}/todos/{todo_id}", status_code=204)
def delete_space_todo(
    todo_id: int,
    space: Space = Depends(get_member_space),
    todo_service: ITodoService = Depends(get_todo_service),
):
    todo_service.delete_space_todo(space_id=space.id, todo_id=todo_id)
