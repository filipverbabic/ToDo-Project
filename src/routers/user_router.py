from fastapi import APIRouter
from fastapi import Depends
from src.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from src.services.user_service import IUserService, get_user_service


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
def get_all_users(service: IUserService = Depends(get_user_service)):
    return service.get_all_users()

@router.get("/{username}", status_code=200, response_model=UserResponse)
def get_user_by_username(username: str, service: IUserService = Depends(get_user_service)):
    return service.get_user_by_username(username)

@router.post("/", status_code=201, response_model=UserResponse)
def create_user(user_data: UserCreate, service: IUserService = Depends(get_user_service)):
    return service.create_user(user_data)

@router.patch("/{user_id}", status_code=200, response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, service: IUserService = Depends(get_user_service)):
    return service.update_user(user_id, user_data)

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, service: IUserService = Depends(get_user_service)):
    service.delete_user(user_id)

