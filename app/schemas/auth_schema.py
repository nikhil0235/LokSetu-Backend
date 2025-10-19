from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class MobileLoginRequest(BaseModel):
    mobile: str

class OTPVerifyRequest(BaseModel):
    mobile: str
    otp: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    fullname: Optional[str]
    username: str
    role: str
    assigned_booths_ids: list
    assigned_constituencies_ids: list
    user_id: int
    phone: Optional[str]
    email: Optional[str]
    created_by: Optional[int]

class OTPResponse(BaseModel):
    message: str
    expires_in: int