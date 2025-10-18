from fastapi import Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings
from app.services.user_service import UserService
from app.services.voter_service import VoterService
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

async def fetch_user_from_token(token: str) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_service = UserService()
    user = user_service.get_user_by_username(username)
    if not user:
        raise credentials_exception 

    return user

async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> User:
    return await fetch_user_from_token(token)

async def get_super_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "super_admin":
        raise HTTPException(status_code=403, detail="Super admin access required")
    return current_user

async def get_admin_or_super_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in ["super_admin", "admin"]:
        raise HTTPException(status_code=403, detail="Admin or super admin access required")
    return current_user

async def get_any_authenticated_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user

def get_voter_service() -> VoterService:
    """Get VoterService instance with constituency file"""
    return VoterService()

