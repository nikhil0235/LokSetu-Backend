from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class SchemeCategory(str, Enum):
    EDUCATIONAL = "Educational"
    SOCIO = "Socio"
    ECONOMIC = "Economic"
    OTHER = "Other"

class SchemeCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: SchemeCategory = SchemeCategory.OTHER

class SchemeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[SchemeCategory] = None

class SchemeResponse(BaseModel):
    scheme_id: int
    name: str
    description: Optional[str]
    category: str
    created_by: Optional[int]
    created_at: str
    updated_at: str

class SchemeBeneficiaryUpdate(BaseModel):
    voter_epic: str
    scheme_ids: List[int]