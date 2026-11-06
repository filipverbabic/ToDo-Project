from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from src.config import SECRET_KEY, TOKEN_EXPIRATION_HOURS
from src.models import User
from src.schemas.user_schema import UserLogin
from src.services.user_service import IUserService, get_user_service


class IAuthService(ABC):
    @abstractmethod
    def generate_token(self, user: User) -> str: ...

    @abstractmethod
    def decode_token(self, token: str) -> dict: ...

    @abstractmethod
    def get_user_from_token(self, token: str) -> User: ...

    @abstractmethod
    def auth_user(self, loginData: UserLogin) -> str: ...

class AuthService(IAuthService):
    def __init__(self, user_service: IUserService):
        self.user_service = user_service

    def generate_token(self, user: User) -> str:
        payload = {
            "user_id": user.id,
            "username": user.username,
            "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRATION_HOURS)
        }

        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired") 
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def get_user_from_token(self, token: str) -> User:
        payload = self.decode_token(token)                                           
        try:                                                                       
            user = self.user_service.get_user_by_id(payload["user_id"])              
        except HTTPException as exc:                                                
            raise HTTPException(status_code=401, detail="Invalid token") from exc     
        if not user.is_active:                                                       
            raise HTTPException(status_code=403, detail="User is inactive")         
        return user   

    def auth_user(self, login_data: UserLogin) -> str:
        user = self.user_service.authenticate_user(login_data)
        return self.generate_token(user)

def get_auth_service(user_service: IUserService = Depends(get_user_service)) -> IAuthService:
    return AuthService(user_service=user_service)

bearer_scheme = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        auth_service: IAuthService = Depends(get_auth_service)
) -> User:
    return auth_service.get_user_from_token(credentials.credentials)