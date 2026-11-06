from fastapi import APIRouter
from fastapi import Depends
from src.models import User
from src.schemas.auth_schema import Token
from src.schemas.user_schema import UserLogin, UserResponse
from src.services.security_service import IAuthService, get_auth_service, get_current_user
from src.services.user_service import IUserService, get_user_service


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(login_data: UserLogin, auth_service: IAuthService = Depends(get_auth_service)):
    token = auth_service.auth_user(login_data)
    return Token(access_token=token)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

