from typing import Optional, List
from datetime import date

class Party:
    def __init__(
        self,
        party_id: int,
        party_name: str,
        party_code: Optional[str] = None,
        party_symbol: Optional[str] = None,
        party_type: Optional[str] = None,
        founded_year: Optional[int] = None,
        is_active: bool = True,
        created_at: Optional[str] = None,
        **kwargs
    ):
        self.party_id = party_id
        self.party_name = party_name
        self.party_code = party_code
        self.party_symbol = party_symbol
        self.party_type = party_type
        self.founded_year = founded_year
        self.is_active = is_active
        self.created_at = created_at

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            party_id=data.get("party_id"),
            party_name=data.get("party_name"),
            party_code=data.get("party_code"),
            party_symbol=data.get("party_symbol"),
            party_type=data.get("party_type"),
            founded_year=data.get("founded_year"),
            is_active=data.get("is_active", True),
            created_at=str(data.get("created_at")) if data.get("created_at") else None
        )

    def to_dict(self):
        return {
            "party_id": self.party_id,
            "party_name": self.party_name,
            "party_code": self.party_code,
            "party_symbol": self.party_symbol,
            "party_type": self.party_type,
            "founded_year": self.founded_year,
            "is_active": self.is_active,
            "created_at": self.created_at
        }

class Alliance:
    def __init__(
        self,
        alliance_id: int,
        alliance_name: str,
        alliance_code: Optional[str] = None,
        description: Optional[str] = None,
        formed_date: Optional[date] = None,
        is_active: bool = True,
        created_at: Optional[str] = None,
        parties: Optional[List[Party]] = None,
        **kwargs
    ):
        self.alliance_id = alliance_id
        self.alliance_name = alliance_name
        self.alliance_code = alliance_code
        self.description = description
        self.formed_date = formed_date
        self.is_active = is_active
        self.created_at = created_at
        self.parties = parties or []

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            alliance_id=data.get("alliance_id"),
            alliance_name=data.get("alliance_name"),
            alliance_code=data.get("alliance_code"),
            description=data.get("description"),
            formed_date=data.get("formed_date"),
            is_active=data.get("is_active", True),
            created_at=str(data.get("created_at")) if data.get("created_at") else None
        )

    def to_dict(self):
        return {
            "alliance_id": self.alliance_id,
            "alliance_name": self.alliance_name,
            "alliance_code": self.alliance_code,
            "description": self.description,
            "formed_date": str(self.formed_date) if self.formed_date else None,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "parties": [party.to_dict() for party in self.parties]
        }