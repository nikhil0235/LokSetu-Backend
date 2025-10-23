from typing import List, Optional
from app.models.scheme import Scheme
from app.data.postgres_adapter import PostgresAdapter
from app.utils.logger import logger

class SchemeService:
    def __init__(self):
        self.adapter = PostgresAdapter()

    def create_scheme(self, scheme_data: dict, created_by: int) -> Scheme:
        """Create a new scheme"""
        scheme_data['created_by'] = created_by
        scheme_dict = self.adapter.create_scheme(scheme_data)
        return Scheme.from_dict(scheme_dict)

    def get_all_schemes(self) -> List[Scheme]:
        """Get all schemes"""
        schemes_data = self.adapter.get_schemes()
        return [Scheme.from_dict(scheme) for scheme in schemes_data]

    def get_scheme_by_id(self, scheme_id: int) -> Optional[Scheme]:
        """Get scheme by ID"""
        scheme_data = self.adapter.get_scheme_by_id(scheme_id)
        if scheme_data:
            return Scheme.from_dict(scheme_data)
        return None

    def update_scheme(self, scheme_id: int, update_data: dict) -> Optional[Scheme]:
        """Update scheme"""
        scheme_data = self.adapter.update_scheme(scheme_id, update_data)
        if scheme_data:
            return Scheme.from_dict(scheme_data)
        return None

    def delete_scheme(self, scheme_id: int) -> bool:
        """Delete scheme and all voter assignments (CASCADE)"""
        success = self.adapter.delete_scheme(scheme_id)
        if success:
            logger.info(f"Deleted scheme {scheme_id} and all voter assignments")
        return success

    def update_voter_schemes(self, voter_epic: str, scheme_ids: List[int], user: dict) -> bool:
        """Update voter's scheme assignments"""
        # Validate that voter exists
        voters = self.adapter.get_voters_by_epic(voter_epic)
        if not voters:
            return False
        
        # Update voter-scheme relationships
        success = self.adapter.update_voter_schemes(voter_epic, scheme_ids, user['user_id'])
        if success:
            logger.info(f"Updated schemes for voter {voter_epic}: {scheme_ids}")
        return success

    def get_voter_schemes(self, voter_epic: str) -> List[dict]:
        """Get schemes assigned to a voter"""
        return self.adapter.get_voter_schemes(voter_epic)

    def get_scheme_beneficiaries(self, scheme_id: int) -> List[dict]:
        """Get voters assigned to a scheme"""
        return self.adapter.get_scheme_beneficiaries(scheme_id)