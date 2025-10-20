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
    party_id: Optional[int] = None
    alliance_id: Optional[int] = None
    party_name: Optional[str] = None
    alliance_name: Optional[str] = None

class OTPResponse(BaseModel):
    message: str
    expires_in: int
    otp: Optional[str] = None
    otp: int