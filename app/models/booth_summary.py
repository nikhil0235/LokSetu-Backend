from typing import Dict, Any
from datetime import datetime

class BoothSummary:
    def __init__(
        self,
        booth_id: str,
        constituency_id: str,
        total_voters: int = 0,
        male_voters: int = 0,
        female_voters: int = 0,
        other_gender_voters: int = 0,
        voting_preference_counts: Dict[str, int] = None,
        religion_counts: Dict[str, int] = None,
        category_counts: Dict[str, int] = None,
        education_counts: Dict[str, int] = None,
        employment_counts: Dict[str, int] = None,
        age_group_counts: Dict[str, int] = None,
        scheme_beneficiaries_counts: Dict[str, Any] = None,
        last_updated: str = None,
        **kwargs
    ):
        self.booth_id = booth_id
        self.constituency_id = constituency_id
        self.total_voters = total_voters
        self.male_voters = male_voters
        self.female_voters = female_voters
        self.other_gender_voters = other_gender_voters
        self.voting_preference_counts = voting_preference_counts or {}
        self.religion_counts = religion_counts or {}
        self.category_counts = category_counts or {}
        self.education_counts = education_counts or {}
        self.employment_counts = employment_counts or {}
        self.age_group_counts = age_group_counts or {}
        self.scheme_beneficiaries_counts = scheme_beneficiaries_counts or {}
        self.last_updated = last_updated or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            booth_id=str(data.get("BoothID")) if data.get("BoothID") else None,
            constituency_id=str(data.get("ConstituencyID")) if data.get("ConstituencyID") else None,
            total_voters=data.get("TotalVoters", 0),
            male_voters=data.get("MaleVoters", 0),
            female_voters=data.get("FemaleVoters", 0),
            other_gender_voters=data.get("OtherGenderVoters", 0),
            voting_preference_counts=eval(data.get("VotingPreferenceCounts", "{}")) if isinstance(data.get("VotingPreferenceCounts"), str) else data.get("VotingPreferenceCounts", {}),
            religion_counts=eval(data.get("ReligionCounts", "{}")) if isinstance(data.get("ReligionCounts"), str) else data.get("ReligionCounts", {}),
            category_counts=eval(data.get("CategoryCounts", "{}")) if isinstance(data.get("CategoryCounts"), str) else data.get("CategoryCounts", {}),
            education_counts=eval(data.get("EducationCounts", "{}")) if isinstance(data.get("EducationCounts"), str) else data.get("EducationCounts", {}),
            employment_counts=eval(data.get("EmploymentCounts", "{}")) if isinstance(data.get("EmploymentCounts"), str) else data.get("EmploymentCounts", {}),
            age_group_counts=eval(data.get("AgeGroupCounts", "{}")) if isinstance(data.get("AgeGroupCounts"), str) else data.get("AgeGroupCounts", {}),
            scheme_beneficiaries_counts=eval(data.get("SchemeBeneficiariesCounts", "{}")) if isinstance(data.get("SchemeBeneficiariesCounts"), str) else data.get("SchemeBeneficiariesCounts", {}),
            last_updated=data.get("LastUpdated")
        )

    def to_dict(self):
        return {
            "BoothID": self.booth_id,
            "ConstituencyID": self.constituency_id,
            "TotalVoters": self.total_voters,
            "MaleVoters": self.male_voters,
            "FemaleVoters": self.female_voters,
            "OtherGenderVoters": self.other_gender_voters,
            "VotingPreferenceCounts": str(self.voting_preference_counts),
            "ReligionCounts": str(self.religion_counts),
            "CategoryCounts": str(self.category_counts),
            "EducationCounts": str(self.education_counts),
            "EmploymentCounts": str(self.employment_counts),
            "AgeGroupCounts": str(self.age_group_counts),
            "SchemeBeneficiariesCounts": str(self.scheme_beneficiaries_counts),
            "LastUpdated": self.last_updated
        }
    
    def to_response_dict(self):
        return {
            "booth_id": self.booth_id,
            "constituency_id": self.constituency_id,
            "total_voters": self.total_voters,
            "male_voters": self.male_voters,
            "female_voters": self.female_voters,
            "other_gender_voters": self.other_gender_voters,
            "voting_preference_counts": self.voting_preference_counts,
            "religion_counts": self.religion_counts,
            "category_counts": self.category_counts,
            "education_counts": self.education_counts,
            "employment_counts": self.employment_counts,
            "age_group_counts": self.age_group_counts,
            "scheme_beneficiaries_counts": self.scheme_beneficiaries_counts,
            "last_updated": self.last_updated
        }