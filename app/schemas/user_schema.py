from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    full_name: Optional[str] = ""
    phone: Optional[str] = ""
    email: Optional[str] = ""
    assigned_booths: Optional[str] = ""
    assigned_constituencies: Optional[str] = ""
    assigned_blocks: Optional[str] = ""
    assigned_panchayats: Optional[str] = ""
    party_id: Optional[int] = None
    alliance_id: Optional[int] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    assigned_booths: Optional[str] = None
    assigned_constituencies: Optional[str] = None
    assigned_blocks: Optional[str] = None
    assigned_panchayats: Optional[str] = None
    party_id: Optional[int] = None
    alliance_id: Optional[int] = None

class UserResponse(BaseModel):
    user_id: int
    username: str
    role: str
    full_name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    assigned_booths: List[str]
    assigned_constituencies: List[str]
    assigned_blocks: List[str]
    assigned_panchayats: List[str]
    created_by: Optional[str]
    party_id: Optional[int] = None
    alliance_id: Optional[int] = None
    party_name: Optional[str] = None
    alliance_name: Optional[str] = None