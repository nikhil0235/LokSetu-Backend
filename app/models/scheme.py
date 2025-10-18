from typing import Optional
from datetime import datetime

class Scheme:
    def __init__(
        self,
        scheme_id: Optional[int] = None,
        name: str = "",
        description: Optional[str] = None,
        category: str = "Other",
        created_by: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        **kwargs
    ):
        self.scheme_id = scheme_id
        self.name = name
        self.description = description
        self.category = category  # Educational, Socio, Economic, Other
        self.created_by = created_by
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            scheme_id=data.get("SchemeID"),
            name=data.get("Name", ""),
            description=data.get("Description"),
            category=data.get("Category", "Other"),
            created_by=data.get("CreatedBy"),
            created_at=data.get("CreatedAt"),
            updated_at=data.get("UpdatedAt")
        )

    def to_dict(self):
        return {
            "SchemeID": self.scheme_id,
            "Name": self.name,
            "Description": self.description,
            "Category": self.category,
            "CreatedBy": self.created_by,
            "CreatedAt": self.created_at,
            "UpdatedAt": self.updated_at
        }

    def to_response_dict(self):
        return {
            "scheme_id": self.scheme_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }