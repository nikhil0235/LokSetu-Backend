from pydantic import BaseModel
from typing import Dict, Optional

class BoothSummaryResponse(BaseModel):
    booth_id: int
    constituency_id: Optional[int]
    total_voters: int
    male_voters: int
    female_voters: int
    other_gender_voters: int
    voting_preference_counts: Dict[str, int]
    religion_counts: Dict[str, int]
    category_counts: Dict[str, int]
    education_counts: Dict[str, int]
    employment_counts: Dict[str, int]
    age_group_counts: Dict[str, int]
    last_updated: Optional[str]
    scheme_beneficiaries_counts: Optional[str]
    class Config:
        from_attributes = True