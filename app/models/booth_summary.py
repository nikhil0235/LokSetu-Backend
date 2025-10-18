from typing import Dict, Any
from datetime import datetime

class BoothSummary:
    def __init__(
        self,
        booth_id: int,
        constituency_id: int = None,
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
        self.scheme_beneficiaries_counts = scheme_beneficiaries_counts or ""
        self.last_updated = last_updated or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def from_dict(cls, data: dict):
        import json
        return cls(
            booth_id=data.get("booth_id"),
            constituency_id=data.get("constituency_id"),
            total_voters=data.get("total_voters", 0),
            male_voters=data.get("male_voters", 0),
            female_voters=data.get("female_voters", 0),
            other_gender_voters=data.get("other_gender_voters", 0),
            voting_preference_counts=data.get("voting_preference_counts", {}) if isinstance(data.get("voting_preference_counts"), dict) else json.loads(data.get("voting_preference_counts", "{}")),
            religion_counts=data.get("religion_counts", {}) if isinstance(data.get("religion_counts"), dict) else json.loads(data.get("religion_counts", "{}")),
            category_counts=data.get("category_counts", {}) if isinstance(data.get("category_counts"), dict) else json.loads(data.get("category_counts", "{}")),
            education_counts=data.get("education_counts", {}) if isinstance(data.get("education_counts"), dict) else json.loads(data.get("education_counts", "{}")),
            employment_counts=data.get("employment_counts", {}) if isinstance(data.get("employment_counts"), dict) else json.loads(data.get("employment_counts", "{}")),
            age_group_counts=data.get("age_group_counts", {}) if isinstance(data.get("age_group_counts"), dict) else json.loads(data.get("age_group_counts", "{}")),
            scheme_beneficiaries_counts=eval(data.get("scheme_beneficiaries_counts", "{}")) if isinstance(data.get("scheme_beneficiaries_counts"), str) else data.get("scheme_beneficiaries_counts", {}),
            last_updated=str(data.get("last_updated")) if data.get("last_updated") else None
        )

    def to_dict(self):
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
            "scheme_beneficiaries_counts": str(self.scheme_beneficiaries_counts),
            "last_updated": self.last_updated
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