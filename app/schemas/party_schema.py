from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class PartyBase(BaseModel):
    party_name: str
    party_code: Optional[str] = None
    party_symbol: Optional[str] = None
    party_type: Optional[str] = None
    founded_year: Optional[int] = None
    is_active: bool = True

class PartyCreate(PartyBase):
    pass

class PartyUpdate(BaseModel):
    party_name: Optional[str] = None
    party_code: Optional[str] = None
    party_symbol: Optional[str] = None
    party_type: Optional[str] = None
    founded_year: Optional[int] = None
    is_active: Optional[bool] = None

class PartyResponse(PartyBase):
    party_id: int
    created_at: Optional[str] = None

    class Config:
        from_attributes = True

class AllianceBase(BaseModel):
    alliance_name: str
    alliance_code: Optional[str] = None
    description: Optional[str] = None
    formed_date: Optional[date] = None
    is_active: bool = True

class AllianceCreate(AllianceBase):
    pass

class AllianceUpdate(BaseModel):
    alliance_name: Optional[str] = None
    alliance_code: Optional[str] = None
    description: Optional[str] = None
    formed_date: Optional[date] = None
    is_active: Optional[bool] = None

class AllianceResponse(AllianceBase):
    alliance_id: int
    created_at: Optional[str] = None
    parties: List[PartyResponse] = []

    class Config:
        from_attributes = True

class PartyAllianceMapping(BaseModel):
    party_id: int
    alliance_id: int
    joined_date: Optional[date] = None
    left_date: Optional[date] = None
    is_current: bool = True