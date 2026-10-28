from fastapi import APIRouter
from fastapi import Depends
from src.schemas.user_schema import UserLogin, UserResponse
from src.services.user_service import IUserService, get_user_service


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=UserResponse)
def login(login_data: UserLogin, service: IUserService = Depends(get_user_service)):
    user = service.authenticate_user(login_data)
    return user

